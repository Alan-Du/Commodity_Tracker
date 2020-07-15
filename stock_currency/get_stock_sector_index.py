#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 11:13:51 2019
Python data reader from Yahoo Finance
@author: shaolun du
@contact: Shaolun.du@gmail.com
"""
import pandas as pd

def get_stock_sector_index_V2(  data, normal=True,
                                sector_weights_dict={},col_order=[],
                                relative = True):
    from Tracker_Central_Dict import stock_sector_dict as s_s_d
    ans = pd.DataFrame()
    for key,val in s_s_d.product_weights_dict.items():
        c_close = data[val[0]]
        c_close = c_close.fillna(method = "backfill")
        ans[key] = c_close.apply(lambda x: sum(x[val[0]]*val[1]),axis=1)
    if len(sector_weights_dict) > 0:
        for key,val in sector_weights_dict.items():
            ans[key] = ans.apply(lambda x: sum(x[val[0]]*val[1]),axis=1)
    if normal:
        ans = ans.divide(ans.iloc[0] / 100)
    if relative:
        temp = ans[ans.columns.difference(['Shanghai'])].div(ans["Shanghai"], axis=0)
        temp["Shanghai"] = ans["Shanghai"]
        ans = temp
    if len(col_order) > 0:  
        ans = ans.sort_index(ascending=False)[col_order]
    ans.index = pd.to_datetime(ans.index).date
    return ans

def industry_lookup(commodity_name):
    from Tracker_Central_Dict import product_dict as p_d
    if commodity_name.upper() in ("AU","AG"):
        return p_d.GOLD
    elif commodity_name.upper() == "CU":
        p_d.COPPER.pop("REAL_ESTATE")
        p_d.COPPER.pop("VOL_TRANS")
        p_d.COPPER.pop("CABLE")
        return p_d.COPPER
    elif commodity_name.upper() == "AL":
        return p_d.ALUMINUM
    elif commodity_name.upper() == "ZN":
        return p_d.ZINC
    elif commodity_name.upper() == "NI":
        return p_d.NI
    elif commodity_name.upper() == "PB":
        return p_d.PB
    elif commodity_name.upper() == "SN":
        return p_d.SN
    elif commodity_name.upper() in ("ZC","J","JM"):
        return p_d.COAL
    elif commodity_name.upper() in ("I","RB","HC"):
        return p_d.STEEL
    elif commodity_name.upper() == "FG":
        return p_d.GLASS
    elif commodity_name.upper() == "TA":
        return p_d.PTA
    elif commodity_name.upper() == "PVC":
        return p_d.PVC
    elif commodity_name.upper() == "PP":
        return p_d.PP
    elif commodity_name.upper() == "PE":
        return p_d.PE
    elif commodity_name.upper() == "RU":
        return p_d.RUBBER
    elif commodity_name.upper() == "MA":
        return p_d.MA
    elif commodity_name.upper() == "BU":
        return p_d.BU
    elif commodity_name.upper() in ("M","RM"):
        return p_d.MEAL
    elif commodity_name.upper() in ("Y","OI","P"):
        return p_d.FOOD_OIL
    elif commodity_name.upper() == "SR":
        return p_d.SUGAR
    elif commodity_name.upper() == "CF":
        return p_d.COTTON
    else:
        return p_d.SH_Index
    return 0
