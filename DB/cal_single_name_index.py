# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 22:27:30 2020

@author: shaol
"""
import pandas as pd
def cal_single_name_index(data, name):
    def cal_roll_yield(x):
        # Helper function after groupby
        if len(x) == 3:
            diffd1 = (x.iloc[1]["Maturity"]-x.iloc[0]["Maturity"]).days/365
            diff1 = (x.iloc[1]["Close"]-x.iloc[0]["Close"])/x.iloc[0]["Close"]
            R1 = diff1/diffd1
            diffd2 = (x.iloc[2]["Maturity"]-x.iloc[1]["Maturity"]).days/365
            diff2 = (x.iloc[2]["Close"]-x.iloc[1]["Close"])/x.iloc[1]["Close"]
            R2 = diff2/diffd2
        elif len(x) == 2:
            diffd1 = (x.iloc[1]["Maturity"]-x.iloc[0]["Maturity"]).days/365
            diff1 = (x.iloc[1]["Close"]-x.iloc[0]["Close"])/x.iloc[0]["Close"]
            R1 = diff1/diffd1
            R2 = 0
        else:
            R1 = 0
            R2 = 0
        return pd.Series({'R1':R1,'R2':R2})
    if len(data) == 0:
        raise Exception("No data captured...")
    data["Code"] = data["Code"].str.strip()
    single = data.loc[data["Code"].str.match(name+"\d+")]
    single = single.sort_values(by=["Dates","OPI"],ascending=False).groupby("Dates").head(3)
    single["Y"] = pd.to_datetime(single["Dates"]).dt.year.astype(str)
    code_len = len(single["Code"].iloc[0].replace(name,""))
    if code_len == 4:
        single["Maturity"] = single["Y"].str[:2]+single["Code"].str.replace(name,"")+"01"
    elif code_len == 3:
        single["Maturity"] = single["Y"].str[:3]+single["Code"].str.replace(name,"")+"01"
    single["Maturity"] = pd.to_datetime(single["Maturity"])
    rolls = single.sort_values(by=["Dates","Maturity"]).groupby("Dates").apply(cal_roll_yield)
    rolls["Close"] = single.groupby("Dates").mean()["Close"]
    rolls["Open"] = single.groupby("Dates").mean()["Open"]
    rolls["Low"] = single.groupby("Dates").mean()["Low"]
    rolls["High"] = single.groupby("Dates").mean()["High"]
    rolls["Vol"] = single.groupby("Dates").mean()["Vol"]
    rolls["OPI"] = single.groupby("Dates").mean()["OPI"]
    rolls["Name"] = name.upper()
    return rolls