# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 09:46:39 2020
Balck Sector analysis scripts
@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
import DB.fetch as fetch
import stock_currency.stock_sector as stock
import single_comm_report as reports

import pandas as pd 
import datetime as dt
import matplotlib.dates as mdates
myFmt = mdates.DateFormatter('%y/%m')
start = dt.datetime(2016, 1, 1).date()

index_data = pd.DataFrame(fetch.get_index_all()).set_index("Dates")

# 10Y bond data
bond_index = index_data[index_data["name"]=="T"][start:]
bond_index["bond_price"] = 0.5*(bond_index["open"]+bond_index["close"])
# AU data
AU_index = index_data[index_data["name"]=="AU"][start:]
AU_index["AU_price"] = 0.5*(AU_index["open"]+AU_index["close"])
# IF data
IF_index = index_data[index_data["name"]=="IF"][start:]
IF_index["IF_price"] = 0.5*(IF_index["open"]+IF_index["close"])
# IC data
IC_index = index_data[index_data["name"]=="IC"][start:]
IC_index["IC_price"] = 0.5*(IC_index["open"]+IC_index["close"])
# I data
I_index = index_data[index_data["name"]=="I"][start:]
I_index["I_price"] = 0.5*(I_index["open"]+I_index["close"])
I_index["I_price"] = I_index["I_price"]/I_index["I_price"].iloc[0]
# RB data
RB_index = index_data[index_data["name"]=="RB"][start:]
RB_index["RB_price"] = 0.5*(RB_index["open"]+RB_index["close"])
RB_index["RB_price"] = RB_index["RB_price"]/RB_index["RB_price"].iloc[0]
# HC data
HC_index = index_data[index_data["name"]=="HC"][start:]
HC_index["HC_price"] = 0.5*(HC_index["open"]+HC_index["close"])
HC_index["HC_price"] = HC_index["HC_price"]/HC_index["HC_price"].iloc[0]
# ZC data
ZC_index = index_data[index_data["name"]=="ZC"][start:]
ZC_index["ZC_price"] = 0.5*(ZC_index["open"]+ZC_index["close"])
ZC_index["ZC_price"] = ZC_index["ZC_price"]/ZC_index["ZC_price"].iloc[0]
# JM data
JM_index = index_data[index_data["name"]=="JM"][start:]
JM_index["JM_price"] = 0.5*(JM_index["open"]+JM_index["close"])
JM_index["JM_price"] = JM_index["JM_price"]/JM_index["JM_price"].iloc[0]
# J data
J_index = index_data[index_data["name"]=="J"][start:]
J_index["J_price"] = 0.5*(J_index["open"]+J_index["close"])
J_index["J_price"] = J_index["J_price"]/J_index["J_price"].iloc[0]

Black_Sector = pd.DataFrame()
Black_Sector["Black_price"] =1/6*(I_index["I_price"]+RB_index["RB_price"]+HC_index["HC_price"]+ZC_index["ZC_price"]+JM_index["JM_price"]+J_index["J_price"])
Black_Sector = Black_Sector.join(bond_index["bond_price"],how="left").fillna(method="bfill")
Black_Sector = Black_Sector.join(AU_index["AU_price"],how="left").fillna(method="bfill")
Black_Sector = Black_Sector.join(IF_index["IF_price"],how="left").fillna(method="bfill")
Black_Sector = Black_Sector.join(IC_index["IC_price"],how="left").fillna(method="bfill")
Black_Sector.to_excel("Black_Sector.xlsx")