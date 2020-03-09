#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 11:13:51 2019
Python data reader from Yahoo Finance
@author: shaolun du
@contact: Shaolun.du@gmail.com
"""
from pandas_datareader import data
import numpy as np
import pandas as pd

product_weights_dict= {
        "AU":[["002237.SZ","600489.SS","600547.SS","600988.SS","002155.SZ"],
              [0.11,0.26,0.29,0.08,0.26]],
        "CU":[["600362.SS","000630.SZ","000878.SZ"],
               [0.3,0.35,0.35]],
        "AL":[["000807.SZ","000933.SZ","000612.SZ"],
              [0.4,0.3,0.3]],
        "ZN":[["600497.SS","000688.SZ","600338.SS",
               "000426.SZ","000960.SZ","601020.SS",
               "601168.SS"],
              [0.2,0.2,0.2,0.1,0.1,0.1,0.1]],
        "PB":[["601020.SS","600497.SS","000688.SZ",
               "600338.SS","000426.SZ","601168.SS"],
              [0.2,0.2,0.2,0.2,0.1,0.1]],
        "SN":[["000960.SZ","000426.SZ"],
              [0.5,0.5,]],
        "NI":[["300208.SZ"],
              [1]],
        "I": [["601969.SS","000655.SZ","000426.SZ",
               "600532.SS"],
              [0.25,0.25,0.25,0.25,]],
        "REBAR":[[ "002110.SZ","600507.SS","600581.SS",],
                 [ 0.4,0.3,0.3 ]],
        "COLS":[[ "002110.SZ","600019.SS","000898.SZ",
                  "000959.SZ","600126.SS","601005.SS",
                  "600581.SS"],
                [ 0.2,0.2,0.2,0.1,0.1,0.1,0.1]],
        "COKE":[[ "601699.SS","600740.SS","603113.SS",
                  "601015.SS","600989.SS"],
                [ 0.2,0.2,0.2,0.2,0.2,]],
        "COAL":[["601225.SS","601898.SS","600188.SS",
                "000933.SZ","600985.SS","601699.SS",
                "603113.SS","601216.SS","000683.SZ",
                "601898.SS"],
                [0.1,0.1,0.1,0.1,0.1,
                 0.1,0.1,0.1,0.1,0.1,]],
        "FG":[[ "601636.SS","000012.SZ","600819.SS",
                "600586.SS"],
              [ 0.25,0.25,0.25,0.25]],
        "PTA":[["603113.SS","601233.SS","000301.SZ",
                "000703.SZ","000936.SZ","600346.SS",
                "002493.SZ"],
               [0.2,0.2,0.2,0.1,0.1,0.1,0.1]],
        "PVC":[["000635.SZ","002092.SZ","002002.SZ",
                "600409.SS","600618.SS","601216.SS"],
               [0.2,0.2,0.2,0.2,0.1,0.1]],
        "PP": [["002648.SZ","600989.SS"],
               [0.5,0.5]],
        "PE": [["600989.SS","600143.SS","300221.SZ"],
               [0.4,0.3,0.3]],
        "RU": [["600500.SS","601118.SS"],
               [0.3,0.7]],
        "BU": [["300135.SZ","002377.SZ"],
               [0.82,0.18]],
        "MA": [["601898.SS","601015.SS","603113.SS",
                "600803.SS","002109.SZ","600722.SS",
                "000683.SZ"],
              [0.2,0.2,0.2,0.1,0.1,0.1,0.1]],
        "MEAL":[["002311.SZ","000876.SZ","600438.SS",
                 "002157.SZ","000702.SZ","002100.SZ",
                 "603668.SS",],
                [0.1,0.3,0.2,0.1,0.1,0.1,0.1]],
        "SUGAR":[["600737.SS","600191.SS","000576.SZ",
                  "000911.SZ","002286.SZ"],
               [0.3,0.1,0.1,0.2,0.3]],
        "COTTON":[["600251.SS","600540.SS","300189.SZ"],
                  [0.1,0.8,0.1]],
        "FOOD_OIL":[["000639.SZ","002852.SZ",
                     "600127.SS","000505.SZ",],
                    [0.1,0.4,0.3,0.2]],
        "DIVIDENS":[[ "000848.SZ","000429.SZ","600873.SS",
                      "603766.SS","603328.SS","600664.SS",
                      "600066.SS","000895.SZ","601088.SS", 
                      "600177.SS"],
                    [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]],
        "Shanghai":[["000001.SS"],
                    [1]],
        }

def cal_index( sector_name,
               Token,Token_weights,
               start_t,end_t,
               normal = True ):
    def weighted(x, cols, w ):
        return np.average(x[cols], weights=w, axis=0)
    c_close = data.get_data_yahoo(symbols=Token, start=start_t, end=end_t)['Adj Close']
    c_close = c_close.fillna(method = "backfill")
    c_close = c_close.sort_index()
    if normal:
        c_close = c_close.divide(c_close.iloc[0] / 100)    
    c_close["Stock_"+sector_name] = c_close.apply(weighted,args=(Token,Token_weights),axis=1)
    return c_close[["Stock_"+sector_name]]

def get_stock_sector_index( start_t, end_t, normal=True,
                            sector_weights_dict={},col_order=[],
                            relative = True):
    def weighted(x, cols, w ):
        return np.average(x[cols], weights=w, axis=0)
    ans = pd.DataFrame()
    for key,val in product_weights_dict.items():
        c_close = data.get_data_yahoo(symbols=val[0], start=start_t, end=end_t)['Adj Close']
        c_close = c_close.fillna(method = "backfill")
        c_close = c_close.sort_index()
        ans[key] = c_close.apply(weighted,args=(val[0],val[1]),axis=1)
    if len(sector_weights_dict) > 0:
        for key,val in sector_weights_dict.items():
            ans[key] = ans.apply(weighted,args=(val[0],val[1]),axis=1)
    if normal:
        ans = ans.divide(ans.iloc[0] / 100)
    if relative:
        temp = ans[ans.columns.difference(['Shanghai'])].div(ans["Shanghai"], axis=0)
        temp["Shanghai"] = ans["Shanghai"]
        ans = temp
    if len(col_order) > 0:    
        ans = ans.sort_index(ascending=False)[col_order]
    return ans
