# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 08:59:17 2019
This program focus on explaining current commodity returns
Target zone narrowed down to four different sector:
    1. Stock market returns
    2. Bond market returns(10Y government bond futures index)
    3. Domestic currency returns

@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
import pandas as pd 
import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import DB.fetch as fetch
import stock_currency.stock_sector as stock
import stock_currency.get_currency as curr

Window = 120 # Correlation test window
end   = dt.date.today() # Date format setting
start = end - timedelta(days=Window)

myFmt = mdates.DateFormatter('%y/%m')
code_map = [ ["IF","Shanghai"],["IH","Shanghai"],["IC","Shanghai"],
             ["T","DIVIDENS"], 
             ["AU","AU"],["AG","AU"],["CU","CU"],["AL","AL"],
             ["ZN","ZN"],["PB","PB"],["SN","SN"],["NI","NI"],
             ["I","I"],["RB","REBAR"],["HC","COLS"],
             ["ZC","COAL"],["JM","COAL"],["J","COKE"],
             ["FG","FG"],
             ["SC","Shanghai"],["TA","PTA"],["PVC","PVC"],["PP","PP"],["PE","PE"],
             ["RU","RU"],["MA","MA"],["BU","BU"],["EG","Shanghai"],["SA","Shanghai"],
             ["A","Shanghai"],["M","MEAL"],["RM","MEAL"],["Y","FOOD_OIL"],["OI","FOOD_OIL"],["P","FOOD_OIL"],
             ["SR","SUGAR"],["CF","COTTON"],["C","Shanghai"],["CS","Shanghai"],["JD","Shanghai"],["AP","Shanghai"],
             ]

answer = []
index_data = pd.DataFrame(fetch.get_index_all()).set_index("Dates").fillna(method="bfill")
inv_df = pd.DataFrame(fetch.get_historical_inventory()).set_index("Dates").fillna(method="bfill")
stock_data = stock.get_stock_sector_index(start,end,False).fillna(method="bfill")
currency = curr.gen_weekly_ccy_df(start,end)[0].fillna(method="bfill")

for sector in code_map:
    comm   = sector[0]
    s_name = sector[1]
    # Data Preparition 
    comm_data = index_data[index_data["name"]==comm].loc[start:end]
    
    bond = index_data[index_data["name"]=="T"].loc[start:end]
    
    inv = inv_df[inv_df["Product"].str.upper()==comm].loc[start:end]["INV"]
    
    stock_df = stock_data[s_name]
        
    cor_stk = comm_data["close"].pct_change().corr(stock_df.pct_change())
    cor_ccy = comm_data["close"].pct_change().corr(currency["CNY_raw"].pct_change())
    cor_bond = comm_data["close"].pct_change().corr(bond["close"].diff()/100)
    cor_USD = comm_data["close"].pct_change().corr(currency["USD_Index"].pct_change())
    
    answer.append({"Name":comm,
                   "Cor_Stock":cor_stk,
                   "Cor_CNY":cor_ccy,
                   "Cor_USD":cor_USD,
                   "Cor_Bond":cor_bond})
format_dict = {'Cor_Stock':'{:.0%}', 'Cor_Bond':'{:.0%}','Cor_USD':'{:.0%}'}
answer = pd.DataFrame(answer).set_index("Name")[["Cor_Stock","Cor_Bond","Cor_CNY","Cor_USD"]]
print(answer)
