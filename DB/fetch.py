# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 14:30:35 2019
Extract data from DB by start date and end date
@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
import DB.dbExecute as db
import datetime as dt
import pandas as pd

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

def get_panel_data(end):
    # Get all historical price for weekly report
    sql_string = "Select * from market where Dates = \'"+str(end)+"\'"
    schema_name = "commodity"
    data = db.dbExecute( schema_name, 
                         sql_string, )
    return data

def get_single_name_index(data, name):
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

def upload_commodity_index( product_name, start = "", end = "" ):
    data = pd.DataFrame(get_historical_all(start,end))
    columns_name = ["Product","Open","High","Low","Close","Vol","OPI","R1","R2"]
    for sector in product_name:
        print("Update:"+sector)
        temp = get_single_name_index(data,sector)
        temp["Product"] = sector.upper()
        temp = temp[columns_name]
        update_commodity_index(temp)

def update_commodity_index( df ):
    # Update weekly commodity index into DB
    schema_name = "commodity"
    for row in df.to_records():
        sql_string = "Replace INTO commodity_index(Dates,name,open,high,low,close,volume,opi,r1,r2) VALUES("
        # Sql generation
        for ele in row:
            try:
                ele = float(ele)
            except:
                if isinstance(ele, str):
                    ele = "'"+ele+"'"
                elif isinstance(ele, dt.date) or isinstance(ele, dt.datetime):
                    ele = "'"+str(ele)+"'"
            sql_string += (str(ele)+",")
           
        sql_string = sql_string[:-1]+")"
        # DB execution
        try:
            db.dbExecute( schema_name,sql_string )
        except:
            pass
        
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

def update_weekly_inventory( df ):
    # Update weekly dataframe into DB
    schema_name = "commodity"
    df = df[["Dates","Product","INV"]]
    for index, row in df.iterrows():
        sql_string = "Replace INTO inventory(Dates,Product,INV) VALUES("
        # Sql generation
        for ele in row:
            try:
                ele = float(ele)
            except:
                if isinstance(ele, str):
                    ele = "'"+ele+"'"
                else:
                    ele = "'"+str(ele)+"'"
            sql_string += (str(ele)+",")
        sql_string = sql_string[:-1]+")"
        # DB execution
        try:
            db.dbExecute( schema_name,sql_string )
        except:
            pass
def update_weekly_commodity( df ):
    # Update weekly dataframe into DB
    schema_name = "commodity"
    for index, row in df.iterrows():
        sql_string = "Replace INTO market(Dates,Code,Open,High,Low,Close,OPI,Vol) VALUES("
        # Sql generation
        for ele in row:
            try:
                ele = float(ele)
            except:
                if isinstance(ele, str):
                    ele = "'"+ele+"'"
                elif isinstance(ele, dt.datetime):
                    ele = "'"+str(ele)+"'"
            sql_string += (str(ele)+",")
           
        sql_string = sql_string[:-1]+")"
        # DB execution
        try:
            db.dbExecute( schema_name,sql_string )
        except:
            pass

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

def update_ccy_price(data):
    # Update weekly dataframe into DB
    data = data.fillna(0)
    schema_name = "commodity"
    for index, row in data.iterrows():
        sql_string = "Replace INTO currency(Dates,USD_Index,USDEUR,USDGBP,USDAUD,CADUSD,JPYUSD,CNYUSD,HKDUSD,TWDUSD,KRWUSD,THBUSD,SGDUSD,MYRUSD,BRLUSD,INRUSD, WTI) VALUES("
        # Sql generation
        if isinstance(index, str):
            sql_string += "'"+index+"',"
        elif isinstance(index, dt.datetime):
            sql_string += "'"+str(index)+"',"
        for ele in row:
            try:
                ele = float(ele)
            except:
                if isinstance(ele, str):
                    ele = "'"+ele+"'"
                elif isinstance(ele, dt.datetime):
                    ele = "'"+str(ele)+"'"
            sql_string += (str(ele)+",")
        sql_string = sql_string[:-1]+")"
        # DB execution
        try:
            db.dbExecute( schema_name,sql_string )
        except:
            print("CCY upload warning Index:"+str(index))
            pass
    return 0

def plot_inv_all(start, end, code_li=[]):
    inv_all = pd.DataFrame()
    code_li = ["au","ag","cu","al","zn","ni","pb","sn",
               "ZC","jm","j","i","hc","rb","FG",
               "TA","pp","pvc","pe","ru","bu","MA",
               "a","m","RM","y","OI","p","CF","SR","c","cs"]
    # plot all inventory data weekly
    inv_df = pd.DataFrame(get_historical_inventory(start, end)).set_index("Dates")
    i = 0
    for code in code_li:
        df_p = inv_df[inv_df["Product"]==code].sort_index()
        df_p[df_p["INV"]<0] = 0
        df_p = df_p.rename(columns={"INV": "INV_"+code})
        if len(inv_all) == 0:
            inv_all["INV_"+code] = df_p["INV_"+code]
        else:
            inv_all = inv_all.join(df_p["INV_"+code], how='outer').fillna(0)
        i = i + 1
    return inv_all
