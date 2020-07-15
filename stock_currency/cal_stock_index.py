#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 11:15:56 2019

@author: shaolundu
@contact: shaolun.du@gmail.com
"""
import pandas as pd
def cal_index_single( sector_name,
                      Token,Token_weights,
                      data, normal = True):
    # calculate function for single name product
    data_df = data[Token]
    data_df = data_df.loc[:,~data_df.columns.duplicated()]
    data_df = data_df.fillna(method = "backfill")
    data_df = data_df.loc[~data_df.index.duplicated()]
    data_df = data_df.sort_index()
    if normal:
        data_df = data_df.divide(data_df.iloc[0] / 100)
    data_df[sector_name] = data_df.apply(lambda x: sum(x[Token]*Token_weights),axis=1)
    data_df.index = pd.to_datetime(data_df.index).date
    return data_df

def get_industry_index( data, ind_dict, relative=False):
    # Get single industry index
    df = pd.DataFrame()
    for name,weights in ind_dict.items():
        t = cal_index_single(name,weights[0],weights[1],data)[name]
        df = df.join(t,how="right")
    if relative:
        df = df.div(df["ShangHai_Index"], axis=0)
    return df