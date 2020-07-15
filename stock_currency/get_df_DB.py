# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 08:24:04 2020
Scripts to generate dataframe from local DB
@author: Shaolun Du
@contact: shaolun.du@gmail.com
"""
import pandas as pd
def get_df_DB(raw_data, ticker_li, sdate, edate):
    # return dataframe based on tickers and dates
    ans = pd.DataFrame()
    raw_data = [ele for ele in raw_data if ele["Date"]>=sdate and ele["Date"]<=edate]
    for target in ticker_li:
        df_data = pd.DataFrame([ele for ele in raw_data if ele["ticker"] == target])
        df_data = df_data[["Date","price"]].set_index("Date")
        df_data = df_data.rename(columns={"price": target})
        ans = ans.join(df_data).fillna(method = "backfill")
    return ans
