#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 11:15:56 2019

@author: shaolundu
@contact: shaolun.du@gmail.com
"""
import numpy as np
import pandas as pd
def weighted(x, cols, w ):
    # Helper function for row based weighted average
    return np.average(x[cols], weights=w, axis=0)
    
def cal_index_single( sector_name,
                      Token,Token_weights,
                      start_t,end_t,
                      normal = True):
    # calculate function for single name product
    from pandas_datareader import data
    data_df = data.get_data_yahoo(symbols=Token, start=start_t, end=end_t)['Adj Close']
    data_df = data_df.fillna(method = "backfill")
    data_df = data_df.sort_index()
    if normal:
        data_df = data_df.divide(data_df.iloc[0] / 100)
    data_df[sector_name] = data_df.apply(weighted,args=(Token,Token_weights),axis=1)
    return data_df

def get_industry_index( start, end, 
                        ind_dict, relative=False):
    # Get single industry index
    df = pd.DataFrame()
    for name,weights in ind_dict.items():
        t = cal_index_single(name,weights[0],weights[1],start,end)[name]
        df = df.join(t,how="right")
    if relative:
        df = df.div(df["ShangHai_Index"], axis=0)
    return df