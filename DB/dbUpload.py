# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 22:15:24 2020

@author: shaolun du
@contact: shaolun.du@gmail.com
"""
import datetime as dt
import pandas as pd
import DB.dbExecute as db
from DB.dbFetch import get_historical_all
from DB.cal_single_name_index import cal_single_name_index

def upload_commodity_index( product_name, start = "", end = "" ):
    data = pd.DataFrame(get_historical_all(start,end))
    columns_name = ["Product","Open","High","Low","Close","Vol","OPI","R1","R2"]
    for sector in product_name:
        print("Update:"+sector)
        temp = cal_single_name_index(data,sector)
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

def update_weekly_commodity( df ):
    # Update weekly dataframe into DB
    schema_name = "commodity"
    for index, row in df.iterrows():
        sql_string = "Replace INTO market(Dates,Code,Open,High,Low,Close,OPI,Vol) VALUES("
        # Sql generation
        sql_string += ("\'"+str(index)+"\',")
        for ele in row:
            try:
                ele = float(ele)
            except:
                if isinstance(ele, str) and len(ele)>1:
                    ele = "'"+ele+"'"
                else:
                    ele = 0
            sql_string += (str(ele)+",")
           
        sql_string = sql_string[:-1]+")"
        # DB execution
        try:
            db.dbExecute( schema_name,sql_string )
        except:
            raise Exception("Upload Error:"+sql_string)

def update_weekly_inventory( df ):
    # Update weekly dataframe into DB
    schema_name = "commodity"
    df = df.reset_index()
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
