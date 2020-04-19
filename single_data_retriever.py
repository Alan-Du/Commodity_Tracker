# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 07:59:36 2020
This is the script to retrieve single name commodity 
data with given frequency 
Input: commodity name code
Output: Formatted dataframe with:
        Price, OPI, VOL, R1, INV, Stock_index, 
        Oil, 10Y bond, CNYUSD, JPYUSD, USD index
@author: Shaolun Du
@contact: Shaolun.du@gmail.com
Commodity code maps see below:
code_map = 
    [["IF","Shanghai"],["IH","Shanghai"],["IC","Shanghai"],
     ["T","DIVIDENS"],
     ["AU","AU"],["AG","AU"],
     ["CU","CU"],["AL","AL"],["ZN","ZN"],
     ["PB","PB"],["NI","NI"],["SN","SN"],
     ["I","I"],["RB","REBAR"],["HC","COLS"],
     ["ZC","COAL"],["JM","COAL"],["J","COKE"],
     ["FG","FG"],["SC","Shanghai"],
     ["TA","PTA"],["PVC","PVC"],["PP","PP"],["PE","PE"],
     ["RU","RU"],["MA","MA"],["BU","BU"],["EG","Shanghai"],["SA","Shanghai"],
     ["A","Shanghai"],
     ["M","MEAL"],["RM","MEAL"],
     ["Y","FOOD_OIL"],["OI","FOOD_OIL"],["P","FOOD_OIL"],
     ["SR","SUGAR"],["CF","COTTON"],
     ["C","Shanghai"],["CS","Shanghai"],
     ["JD","Shanghai"],["AP","Shanghai"],
     ]
"""
import DB.fetch as fetch
import stock_currency.stock_sector as stock
import single_comm_helper as rep_helper

import pandas as pd 
import datetime as dt
import matplotlib.dates as mdates
myFmt = mdates.DateFormatter('%y/%m')
# Date format setting
start = dt.datetime(2016, 1, 1).date()
end = dt.date.today()
Save_df = False
N = 180
frequency = "D"
commodity_name = "TA"
Relative_Switch = False
# Commodity index data
index_data = pd.DataFrame(fetch.get_index_all()).set_index("Dates")
# 10Y bond data
bond_index = index_data[index_data["name"]=="T"][start:end]
bond_index["bond_price"] = 0.5*(bond_index["open"]+bond_index["close"])
# Commodity inventry data
inv_df = pd.DataFrame(fetch.get_historical_inventory()).set_index("Dates")
# Commodity related stock sector data
industry_weights_dict = stock.industry_lookup(commodity_name)
stock_data = stock.get_single_industry_index(start,end,True,industry_weights_dict,[],Relative_Switch).add_prefix('stock_')
stock_name = list(stock_data.columns.values)
stock_name.remove('stock_ShangHai_Index')
# Currency data
currency_data = pd.DataFrame(fetch.get_histroical_ccy(start,end)).set_index("Dates")
currency_data = currency_data[["USD_Index","CNYUSD","JPYUSD","WTI"]]
# Get market data
market = index_data[index_data["name"]==commodity_name][start:end]
market["VOL/OPI"] = market["volume"]/market["opi"]
market["mid_price"] = 0.5*(market["open"]+market["close"])
market = market[["mid_price","opi","volume","r1","r2","VOL/OPI"]]
# Get inventory data
inventory = inv_df.loc[inv_df["Product"].str.upper()==commodity_name][start:end]["INV"]
market = market.join(bond_index["bond_price"],how="left")
market = market.join(inventory,how="left")
market = market.join(stock_data,how="left")
market = market.join(currency_data,how="left")
market = market.fillna(method="ffill")
market = market.fillna(method="bfill")

fig = rep_helper.single_stock_analyze(commodity_name, stock_name, market, N)

# Turn on if want to save the data frame
if Save_df:
    writer = pd.ExcelWriter(commodity_name+'_Data.xlsx',engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet(commodity_name+"_Market")
    writer.sheets[commodity_name+"_Market"] = worksheet
    market.to_excel(writer,sheet_name=commodity_name+"_Market",startrow=0 , startcol=0)

    writer.save()