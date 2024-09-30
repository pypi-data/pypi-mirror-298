import polars as pl
from datetime import datetime, timedelta
from tqdm import tqdm
import sys
import lyytools
import lyystkcode
import lyywmdf
import traceback
import lyybinary
import os
import lyyztreason
from lyylog import log
import lyycfg
import pandas as pd
import time


api_dict = {}
signal_id_dict = {"昨日换手": 777, "昨日回头波": 776}  # ,"涨停原因":888
column_mapping = {"时间": "datetime", "代码": "code", "名称": "name", "开盘": "open", "今开": "open", "收盘": "close", "最新价": "close", "最高": "high", "最低": "low", "涨跌幅": "change_rate", "涨跌额": "change_amount", "成交量": "vol", "成交额": "amount", "振幅": "amplitude", "换手率": "turnover_rate"}

tdx_path = r"D:\Soft\_Stock\通达信金融终端(开心果交易版)V2024.09"

k_type = {"5min":0,"15min":1,"30min":2,"60min":3,"day2":4,"week":5,"month":6,"1min":7,"1mink":8,"day":9,"season":10,"year":11}



def get_dict_all_code_guben():
    df_all_cache_file = r"D:\UserData\resource\data\df_all_info.pkl"
    df_all_info = pd.read_pickle(df_all_cache_file)
    dict_all_code_guben = df_all_info.set_index("code")["流通股本亿"].to_dict()
    return dict_all_code_guben


def update_cg_series(df, debug=False):
    if len(df) < 10000:
        print("dataframe<1000 line，check it")
    df_grouped = df.groupby("code")

    for code, group_rows in df_grouped:
        if debug:
            print("enter for code,group_rows in df_grouped")
        market = lyystkcode.get_market(code)
        tdx_signal_file = os.path.join(tdx_path, rf"T0002\signals\signals_user_{999}", f"{market}_{code}.dat")
        db_last_date_int = lyybinary.get_lastdate_tdx_sinal(tdx_signal_file)
        if debug:
            print(f"try to filter: group_rows['dayint'] > {db_last_date_int}")
        filtered_rows = group_rows.filter(pl.col("dayint") > db_last_date_int)
        if debug:
            print(filtered_rows)
        data_dict = filtered_rows.select(["dayint", "chonggao"]).to_dict(as_series=False)
        data_dict = dict(zip(data_dict["dayint"], data_dict["chonggao"]))

        if debug:
            print(tdx_signal_file, db_last_date_int, "db_last_date_int type=", type(db_last_date_int))
        lyybinary.add_data_if_new_than_local(tdx_signal_file, data_dict, db_last_date_int, debug=debug)
        if debug:
            print("写入文件成功")

def get_ztreason_df(debug=False):
    lyycfg.cfg.get_engine_conn()
    query = """SELECT * FROM (SELECT *,ROW_NUMBER() OVER (PARTITION BY code ORDER BY date DESC) AS rn FROM stock_jiucai WHERE date >= DATE_SUB(CURDATE(), INTERVAL 20 DAY)) AS subquery WHERE rn = 1 """
    result = pl.read_database(query, lyycfg.cfg.engine)
    result = result.with_columns([
        pl.col("code").cast(pl.Utf8).str.zfill(6),
        pl.lit(888).alias("signal_id"),
        pl.lit(0.000).alias("number"),
        (pl.col("plate_name").cast(pl.Utf8) + "：" + pl.col("reason").cast(pl.Utf8).str.replace("\n", "")).alias("text"),
        pl.col("code").apply(lyystkcode.get_market).alias("market")
    ])
    return_df = result.select(["market", "code", "signal_id", "text", "number"])
    if debug:
        print(return_df)
    return return_df

def update_signal_txt(df, debug=False):
    if debug:
        print("enter update_signal_txt, input para len=", len(df))
    grouped_df = df.groupby("code").agg([
        pl.col("volume").last(),
        pl.col("huitoubo").last(),
        pl.col("dayint").last()
    ])

    df_reason = get_ztreason_df()
    if debug:
        print("apply code 666 to grouped_df")
        print(grouped_df, "----------------here is grouped df---------------")
    
    data_list = []
    pbar = tqdm(range(len(grouped_df)), desc="update_chonggao_huitoubo_for_signal_txt")
    dict_all_code_guben = get_dict_all_code_guben()
    for row in grouped_df.iter_rows(named=True):
        pbar.update(1)
        code = row["code"]
        market = lyystkcode.get_market(code)
        volume = row["volume"]
        huitoubo = row["huitoubo"]
        
        cg_dict = {
            "market": market,
            "code": code,
            "signal_id": 666,
            "text": "",
            "number": (volume / 100) / dict_all_code_guben.get(code, 1)
        }
        
        ht_dict = {
            "market": market,
            "code": code,
            "signal_id": 665,
            "text": "",
            "number": huitoubo
        }
        
        data_list.append(cg_dict)
        data_list.append(ht_dict)
        time.sleep(0.01)

    if debug:
        print("concat df_chonggao,df_huitoubo,df_reason")
    df_merged = pl.concat([pl.DataFrame(data_list), df_reason]).sort("signal_id")

    if debug:
        print("contact finished. Try to filter no gbk code")
    df_merged = df_merged.with_columns(
        pl.when(pl.col("").is_in([pl.Utf8, pl.Categorical]))
        .then(pl.col("").str.encode("gbk", errors="ignore").str.decode("gbk"))
        .otherwise(pl.col(""))
    )
    path = os.path.join(tdx_path, r"T0002/signals/extern_user.txt")
    df_merged.write_csv(path, separator="|", has_header=False, encoding="gbk")
    if debug:
        print("执行完成！df_merged=\n", df_merged)
    return df_merged



def df_add_notfull(df, haveto_date, debug=False):
    now = datetime.now()
    today_date_int = now.year * 10000 + now.month * 100 + now.day
    
    df = df.with_columns([
        pl.col("day").str.replace("-", "").cast(pl.Int32).alias("dayint"),
        pl.lit(15).alias("notfull")
    ])
    
    if df["dayint"].max() == today_date_int and now.hour < 15:
        if debug:
            print(f"今天没收盘，要重点标记一下。today_time_hour={now.hour}, today_date_int={today_date_int}")
        df = df.with_columns(
            pl.when(pl.col("dayint") == today_date_int)
            .then(now.hour)
            .otherwise(pl.col("notfull"))
            .alias("notfull")
        )
    else:
        if debug:
            print("in df_add_notfull, 完美收盘无需牵挂", end="")
    return df

def 通达信下载原始分钟K线(api, 股票数字代码, 要下载的K线数量, ktype='15min', start_index=0, debug=False) -> pl.DataFrame:
    fun_name = sys._getframe().f_code.co_name
    t0 = datetime.now()
    if debug:
        print("函数名：", fun_name)
    
    市场代码 = lyystkcode.get_market(股票数字代码)
    if debug:
        print(f"市场代码={市场代码}，股票数字代码={股票数字代码},{k_type[ktype]},要下载的K线数量={要下载的K线数量}")
    
    print(f"开始下载：{股票数字代码}")
    df_tdx = pl.DataFrame(api.to_df(api.get_security_bars(k_type[ktype], 市场代码, 股票数字代码, start_index, 要下载的K线数量)))
    print(f"下载完成：{股票数字代码}")
    
    return df_tdx

def 分钟线合成日K(df) -> pl.DataFrame:
    所有分钟线 = df.clone()
    所有分钟线 = 所有分钟线.with_columns(pl.col("day").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M"))
    完美日K线 = 所有分钟线.groupby_dynamic("day", every="1d").agg([
        pl.col("open").first().alias("open"),
        pl.col("high").max().alias("high"),
        pl.col("low").min().alias("low"),
        pl.col("close").last().alias("close"),
        pl.col("volume").sum().alias("volume")
    ]).drop_nulls()
    完美日K线 = 完美日K线.with_columns(pl.col("day").dt.date())
    return 完美日K线

def 分钟线5合15(所有分钟线) -> pl.DataFrame:
    多分钟K线 = 所有分钟线.groupby_dynamic("day", every="15m").agg([
        pl.col("open").first().alias("open"),
        pl.col("high").max().alias("high"),
        pl.col("low").min().alias("low"),
        pl.col("close").last().alias("close"),
        pl.col("volume").sum().alias("volume")
    ]).drop_nulls()
    
    多分钟K线 = 多分钟K线.with_columns([
        pl.col("day").dt.strftime("%H%M").alias("time"),
        pl.col("day").dt.date().alias("day")
    ])
    
    十点K线 = 多分钟K线.filter(pl.col("time") == "1000").select(["time", "day", "high"])
    return 十点K线

def 多周期K线合并(完美日K线, 十点K线, debug=False) -> pl.DataFrame:
    多周期合成K线 = 完美日K线.join(十点K线.rename({"high": "tenhigh"}), on="day")
    
    # 注意：这里的 MyTT.REF 需要替换为 Polars 的等效操作
    多周期合成K线 = 多周期合成K线.with_columns([
        ((pl.col("high") / pl.col("close").shift(1) - 1) * 100).round(2).alias("up"),
        ((pl.col("tenhigh") / pl.col("close").shift(1) - 1) * 100).round(2).alias("chonggao"),
        ((1 - pl.col("close") / pl.col("high")) * 100).round(2).alias("huitoubo")
    ])
    
    if debug:
        print("多周期合成K线=", 多周期合成K线.select("chonggao"))
    
    return 多周期合成K线

def 原始分钟df格式化(原始分钟df, debug=False):
    原始分钟df = 原始分钟df.drop(["amount", "year", "month", "day", "hour", "minute"])
    原始分钟df.columns = ['open', 'close', 'high', 'low', 'volume', 'day']
    
    原始分钟df = 原始分钟df.with_columns([
        pl.col("close").shift(1).alias("shiftc"),
        pl.when(pl.col("close") > pl.col("close").shift(1))
          .then(pl.col("close"))
          .otherwise(pl.col("close").shift(1))
          .alias("up")
    ])
    
    所有分钟线 = 原始分钟df.clone()
    所有分钟线 = 所有分钟线.with_columns(pl.col("day").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M"))
    
    新日K = 分钟线合成日K(所有分钟线)
    新15分钟K = 分钟线5合15(所有分钟线)
    
    完美df = 多周期K线合并(新日K, 新15分钟K)
    
    完美df = 完美df.with_columns([
        (pl.col("volume") / 10000).cast(pl.Int32).alias("volume"),
        pl.col("day").dt.strftime("%Y%m%d").cast(pl.Int32).alias("dayint"),
        pl.col("day").dt.strftime("%Y-%m-%d").alias("day")
    ])
    
    return 完美df

def wmdf(api, stk_code_num, to_down_kline, server_ip=None, debug=False) -> pl.DataFrame:
    if debug:
        print(f"函数名：{sys._getframe().f_code.co_name}: try to get wmdf")
    t0 = datetime.now()
    try:
        if debug:
            print(f"准备开始下载原始K线，IP={api.ip}")
        
        df = 通达信下载原始分钟K线(api, stk_code_num, to_down_kline, debug=debug)
        
        time = datetime.now() - t0
        if time > timedelta(seconds=0.3):
            print(f"通达信下载原始K线下载时间过长,IP={api.ip} {time}")
            return None
        else:
            print(time)
        
        if df.is_empty():
            raise Exception("通达信下载原始分钟K线 error: DataFrame must not be empty")
    except Exception as e:
        print(f"Function: wmdf, try to run 通达信下载原始分钟线 error。stk_code_num: {stk_code_num}, to_down_kline: {to_down_kline}, api: {api}, {e}")
        print(f"wmdf error: {e}")
        return None
    
    if debug:
        lyytools.测速(t0, "通达信下载原始K线")
    t1 = datetime.now()
    
    try:
        wmdf = 原始分钟df格式化(df)
        if debug:
            print(wmdf)
    except Exception as e:
        print(f"error函数名：{sys._getframe().f_code.co_name}: try to get wmdf")
        print(f"api={api}, stk_code_num={stk_code_num}, to_down_line={to_down_kline}, try to run wmdf = 原始分钟df格式化(df) error: {e}")
        return None
    
    if debug:
        lyytools.测速(t1, "df格式转换")
    return wmdf

def get_and_format_wmdf_for_single_code(code, api, db_last_date_int, kline_n, debug=False):
    if debug:
        print(f"get_and_format_wmdf_for_single_code：{code}, {api}, {db_last_date_int}, {kline_n}")
    now = datetime.now()
    today_date_int = now.year * 10000 + now.month * 100 + now.day
    if debug:
        print(f"# 初始化api连接, {code}")
    
    try:
        wmdf_data = wmdf(api, code, kline_n, debug=debug)
    except Exception as e:
        traceback.print_exc()
    
    if debug:
        print(wmdf_data.tail(1))
    
    wmdf_data = wmdf_data.with_columns(pl.lit(code).alias("code"))
    
    if debug:
        print(f"in function get_and_format_wmdf_for_single_code,{code} wmdf = \n", wmdf_data)
    
    wmdf_data = df_add_notfull(wmdf_data, today_date_int)
    wmdf_data = wmdf_data.slice(1)
    
    if debug:
        print(wmdf_data.columns)
        print(wmdf_data.tail(1))
    
    filtered_df = wmdf_data.filter(pl.col("dayint") > db_last_date_int)
    return filtered_df

def update_wmdf_closed(wmdf_closed, code_api_dict, debug=False):
    df_to_concat_list = [wmdf_closed]
    grouped = wmdf_closed.groupby("code").agg(pl.col("dayint").max().alias("max_dayint"))
    last_date_dict = grouped.select(["code", "max_dayint"]).to_dict(as_series=False)
    last_date_dict = dict(zip(last_date_dict["code"], last_date_dict["max_dayint"]))
    code_name_dict = lyystkcode.get_code_name_dict()
    pbar = tqdm(total=len(code_api_dict), desc="update wmdf closed")

    if debug:
        print("enter fun: lyydata.update_wmdf_closed")
    if code_api_dict is None:
        if debug:
            print("code_api_dict is None, return")
        return

    for index, (code, api) in enumerate(code_api_dict.items()):
        pbar.update(1)
        db_last_date_int, 相差天数, kline_n = lyywmdf.calc_lastdate_kline_number(code, last_date_dict, debug=debug)
        if 相差天数 == 0:
            if debug:
                print("新", end="")
            continue
        try:
            if debug:
                print(f"code/type={code} {type(code)}, server_ip={api.ip}, dblast_date/type={db_last_date_int} {type(db_last_date_int)}, 相差天数={相差天数}, kline_n={kline_n}")
            if code is None or api is None or kline_n is None or db_last_date_int is None:
                print("code/api/kline_n/db_last_date_int is None, continue")
                continue

            df_single = get_and_format_wmdf_for_single_code(code, api, db_last_date_int, kline_n, debug=False)
            df_single = df_single.with_columns(pl.lit(code_name_dict.get(code, "")).alias("name"))
            if debug:
                print(df_single, "df_single")
        except Exception as e:
            traceback.print_exc()
            log(f"{code}{api.ip}{str(db_last_date_int)}{str(kline_n)}{str(e)}")
            continue
        if debug:
            print(f"finish code={code}")
        if not df_single.is_empty():
            if debug:
                print("add df_single to df list")
            df_to_concat_list.append(df_single)
            if debug:
                print("finish add df_single to df list")
        else:
            if debug:
                log(f"{code}@{api.ip} df_single is empty")

    wmdf_closed = pl.concat(df_to_concat_list)
    if debug:
        print("wmdf_closed\n", wmdf_closed)
    pbar.close()
    if debug:
        print("return wmdf_closed")
    return wmdf_closed


if __name__ == "__main__":
    # 初始化模拟环境
    api = MockAPI("127.0.0.1")
    code = "000001"
    code_api_dict = {code: api}

    # 创建初始的 wmdf_closed
    initial_data = {
        "code": [code],
        "dayint": [20230101],
        "open": [15.0],
        "high": [16.0],
        "low": [14.0],
        "close": [15.5],
        "volume": [5000],
        "name": ["示例股票"]
    }
    wmdf_closed = pl.DataFrame(initial_data)

    # 运行更新函数
    updated_wmdf = update_wmdf_closed(wmdf_closed, code_api_dict, debug=True)

    # 打印结果
    print("Updated WMDF:")
    print(updated_wmdf)

    # 显示统计信息
    print("\nStatistics:")
    print(updated_wmdf.describe())

    # 显示最新的几条记录
    print("\nLatest records:")
    print(updated_wmdf.tail(5))


