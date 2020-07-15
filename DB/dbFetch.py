# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 14:30:35 2019
Extract data from DB by start date and end date
@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
import DB.dbExecute as db
def get_commodity_all():
    sql_str = "Select * from market where close > 0"
    schema_name = "commodity"
    data = db.dbExecute(schema_name,sql_str)
    return data

def get_historical_single(start, end,
                          code ):
    # Get all historical price for weekly report
    sql_string = "Select * from market where Dates >=\'"+str(start)+"\' and Dates <=\'"+\
                str(end)+"\'"+" and Close > 0 and Code LIKE '%"+code+"%'"
    schema_name = "commodity"
    data = db.dbExecute( schema_name, 
                         sql_string, )
    return data
def get_historical_all( start = "", end = "" ):
    # Get all historical price for weekly report
    if start != "":
        sql_string = "Select * from market where Dates >=\'"+str(start)+"\' and Dates <=\'"+\
                    str(end)+"\'"+" and Close > 0"
    else:
        sql_string = "Select * from market where Close > 0"
    schema_name = "commodity"
    data = db.dbExecute( schema_name, 
                         sql_string, )
    return data

def get_panel_data():
    # Get all historical price for weekly report
    sql_string = "Select * from market where Dates = (select MAX(Dates) from market)"
    schema_name = "commodity"
    data = db.dbExecute( schema_name, 
                         sql_string, )
    return data
        
def get_index_all( start = "", end = "" ):
    # Get all historical commodity_index for weekly report
    if start != "":
        sql_string = "Select * from commodity_index where Dates >=\'"+str(start)+"\' and Dates <=\'"+\
                    str(end)+"\'"+" and Close > 0"
    else:
        sql_string = "Select * from commodity_index where Close > 0"
    schema_name = "commodity"
    data = db.dbExecute( schema_name, 
                         sql_string, )
    return data

def get_historical_inventory(start="", end=""):
    # Get all historical price for weekly report
    if start =="":
        sql_string = "Select * from inventory"
    else:
        sql_string = "Select * from inventory where Dates >=\'"+\
                str(start)+"\' and Dates <=\'"+str(end)+"\'"
    schema_name = "commodity"
    data = db.dbExecute( schema_name, 
                         sql_string, )
    return data
def gen_weekly_ccy_df( start,end ):
    """ Generate weekly ccy data table
    """
    currency_li =[ "USD_Index",
                   "EURUSD","GBPUSD","AUDUSD","CADUSD",
                   "JPYUSD",
                   "CNYUSD","HKDUSD","TWDUSD",
                   "KRWUSD","THBUSD","SGDUSD","MYRUSD",
                   "BRLUSD","INRUSD",
                   "CNY_raw","JPY_raw"
                  ]
    currency_df = get_histroical_ccy(start,end)
    temp = currency_df[["JPYUSD","CNYUSD"]]
    currency_df["EURUSD"] = 1/currency_df["USDEUR"]
    currency_df["GBPUSD"] = 1/currency_df["USDGBP"]
    currency_df["AUDUSD"] = 1/currency_df["USDAUD"]
    currency_df = currency_df/currency_df.iloc[0]
    currency_df["CNY_raw"] = temp["CNYUSD"]
    currency_df["JPY_raw"] = temp["JPYUSD"]
    return currency_df[currency_li],currency_li

def get_histroical_ccy( start, end ):
    # Get all historical price in currency sector
    sql_string = "Select * from currency where Dates >=\'"+\
                str(start)+"\' and Dates <=\'"+ str(end)+"\'"
    schema_name = "commodity"
    data = db.dbExecute( schema_name, 
                         sql_string, )
    return data

def get_ccy_price( start, end ):
    """ Get currency price with pandas from Fed reserve
    """
    from pandas_datareader import data
    currency_li =["DTWEXBGS","DEXUSEU","DEXUSUK","DEXUSAL",
                  "DEXCAUS","DEXJPUS","DEXCHUS","DEXHKUS",
                  "DEXTAUS","DEXKOUS","DEXMAUS","DEXTHUS",
                  "DEXSIUS","DEXINUS","DEXBZUS","DCOILWTICO",
                  ] 
    currency_rename = { "DTWEXBGS":"USD_Index","DEXUSEU":"USDEUR",
                        "DEXUSUK":"USDGBP","DEXUSAL":"USDAUD","DEXCAUS":"CADUSD",
                        "DEXCHUS":"CNYUSD","DEXJPUS":"JPYUSD","DEXTHUS":"THBUSD","DEXTAUS":"TWDUSD",
                        "DEXHKUS":"HKDUSD","DEXMAUS":"MYRUSD","DEXSIUS":"SGDUSD",
                        "DEXKOUS":"KRWUSD","DEXBZUS":"BRLUSD","DEXINUS":"INRUSD",
                        "DCOILWTICO":"WTI",}
    currency_df = data.get_data_fred( currency_li, start, end).fillna(method="backfill")
    currency_df = currency_df.rename(columns=currency_rename)
    return currency_df
