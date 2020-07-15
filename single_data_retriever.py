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

import pandas as pd 
import datetime as dt
import matplotlib.dates as mdates
from Analyzer.get_single_commodity import get_single_commodity
from Analyzer.get_stock_by_commodity import get_stock_by_commodity

myFmt = mdates.DateFormatter('%y/%m')
# Date format setting
start = dt.datetime(2015, 1, 1).date()
end = dt.date.today()
Save_df = False
Relative_Switch = True
N = 180
frequency = "D"
commodity_name = "AU"
comm_data = get_single_commodity( start, end, commodity_name, True )
stock_data = get_stock_by_commodity(start, end, commodity_name)
comm_data = comm_data.join(stock_data, how="left").fillna(method="backfill")
comm_data.to_excel("Data.xlsx")
