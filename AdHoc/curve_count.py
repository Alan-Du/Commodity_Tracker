# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 14:13:37 2020
Test for each sector of curve structure
@author: Shaolun Du
"""
import DB.fetch as fetch
import stock_currency.stock_sector as stock
import stock_currency.industry_tracking as ind_tracking
import stock_currency.stock_tracking as stock_tracking

import pandas as pd 
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
start = dt.datetime(2014, 1, 1).date()
end = dt.date.today()
myFmt = mdates.DateFormatter('%y/%m')
col_names = { "Material":["Chemicals","Metals","Paper","Steel","Architecture"],
              "Discretionary":["Cars","Cloth","Media","Home_Appliance"],
              "Non-Discretionary":["Food","Wine","Beverage","Medicine","Retail"],
              "Energy":["Oil_Gas","Coal","Energy_Facility"],
              "Finance":["Bank","Insurance","Securities","Financial_Service"],
              "Medical":["Medical","Medical_Service","Biotechnology"],
              "Transportation":["Trans_Port","Trans_Road","Aviation","National_Defense"],
              "Computer":["IT_Software","IT_Hardware"],
              "Tel-Commu":["Communication_Equipment","Tel_Service","Electronic"],
              "Water-Energy":["Elec_Power","Water_Gas"],
              "Construction":["Urban_Construction","Development"],
              "Dividend":["Dividends"],
             }
code_map = [ ["IF","Shanghai"],["IH","Shanghai"],["IC","Shanghai"],
             ["T","DIVIDENS"], 
             ["AU","AU"],["AG","AU"],
             ["CU","CU"],["AL","AL"],["ZN","ZN"],
             ["PB","PB"],["SN","SN"],["NI","NI"],
             ["I","I"],["RB","REBAR"],["HC","COLS"],
             ["ZC","COAL"],["JM","COAL"],["J","COKE"],
             ["FG","FG"],
             ["SC","Shanghai"],["TA","PTA"],["PVC","PVC"],["PP","PP"],["PE","PE"],
             ["RU","RU"],["MA","MA"],["BU","BU"],["EG","Shanghai"],["SA","Shanghai"],
             ["A","Shanghai"],["M","MEAL"],["RM","MEAL"],["Y","FOOD_OIL"],["OI","FOOD_OIL"],["P","FOOD_OIL"],
             ["SR","SUGAR"],["CF","COTTON"],["C","Shanghai"],["CS","Shanghai"],["JD","Shanghai"],["AP","Shanghai"],
             ]
secotrs = {
        "Stock":["IF","IH","IC"],
        "Matels":["CU","AL","ZN","PB","SN","NI"],
        "Black":["I","RB","HC","ZC","JM","J"],
        "Chem":["TA","PVC","PP","PE","RU","MA","BU"],
        "Agri":["A","M","RM","Y","OI","P","SR","CF","C","CS"],
        }
index_data = pd.DataFrame(fetch.get_index_all()).set_index("Dates")
index_data = index_data[start:].reset_index()
df = pd.DataFrame()
for sector,names in secotrs.items():
    sector_comm = index_data[index_data['name'].isin(names)]
    sector_prob = sector_comm[["Dates","r1"]].groupby(["Dates"]).apply(lambda x: pd.Series((x["r1"] > 0).sum()/(x["r1"]).count())).unstack()
    sector_prob = sector_prob.rename(sector)
    df[sector]  = sector_prob
    
df.to_excel("curve_prob.xlsx")


