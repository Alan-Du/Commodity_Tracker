# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 02:52:17 2019

@author: shaolun Du
@contact:Shaolun.du@gmail.com
"""
import stock_currency.industry_dict as I_D
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


def get_industry_data( start,
                       end, 
                       relative=False):
    dictionary_all = {}
    col_names = ["Chemicals","Metals","Paper","Steel","Architecture","Cars","Cloth","Media","Home_Appliance",
                 "Food","Wine","Beverage","Medicine","Retail","Oil_Gas","Coal","Energy_Facility",
                 "Bank","Insurance","Securities","Financial_Service","Medical","Medical_Service",
                 "Biotechnology","Trans_Port","Trans_Road","Aviation","National_Defense","IT_Hardware",
                 "IT_Software","Communication_Equipment","Tel_Service","Electronic","Elec_Power","Water_Gas",
                 "Urban_Construction","Development","Dividends"]
    for dd in [I_D.MATERIALS,I_D.Consumer_Discretionary,
               I_D.Consumer_Staples,I_D.Energy,I_D.Finance,
               I_D.Medical_Health,I_D.Industry,I_D.Information_Technology,
               I_D.Utilities,I_D.Real_Estate,I_D.Dividend]:
        dictionary_all.update(dd)
    df = get_industry_index(start,end,dictionary_all,relative)
    df = df[col_names]
    return df
