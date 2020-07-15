# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 06:55:11 2020
Stock price upload object
@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
import math
import pandas as pd
import DB.dbExecute as db
import yfinance as yf
import stock_currency.stock_tickers as tickers
class stock_handler():
    def __init__(self):
        self.__sql_format = "Replace INTO stock_close(Date,ticker,price) VALUES(\"{}\",\"{}\",{})"
        self.__sql_download = "Select * from stock_close where Date >=\"{}\" and Date <=\"{}\""
        self.__schema_name = "commodity"
        self.__log_name = "Error_Log.txt"
        self.__s_tickers = tickers.stock_tickers
        self.__error_msg = []
    
    def _upload_all_ticker(self, start_t, end_t, use_tickers=""):
        if use_tickers != "":
            self.__s_tickers = use_tickers
        for ticker in self.__s_tickers:
            print("Download:{}".format(ticker))
            data = self._download(ticker,start_t,end_t)
            self._upload_db(ticker,data)
        self._write_into_log()
        
    def _gen_all_ticker_df(self, start_t, end_t):
        data = self._download_db(self.__s_tickers,start_t,end_t)
        data_df = self._gen_df(self.__s_tickers,data)
        return data_df
    
    def _download(self, ticker, start_t, end_t):
        data = yf.download(tickers=ticker, start=start_t, end=end_t)['Adj Close']
        return data
    
    def _upload_db(self,ticker,data):
        for Date, Value in data.items():
            if not math.isnan(Value):
                sql_string = self.__sql_format.format(Date,ticker,Value)
                db.dbExecute( self.__schema_name, sql_string )
            else:
                msg_string = "Ticker:{},Date:{},Missing Data".format(ticker,Date)
                self.__error_msg.append(msg_string)
                print(msg_string)
                continue
    
    def _write_into_log(self):
        with open("Error_MSG.txt", "w") as text_file:
            for msg in self.__error_msg:
                text_file.write(msg)
                text_file.write("\n")
        text_file.close()
        
    def _download_db(self, tickers, start_t, end_t):
        sql_download = self.__sql_download.format(start_t,end_t)
        data = db.dbExecute( self.__schema_name, sql_download )
        data = [ele for ele in data if ele["ticker"] in tickers]
        return data
    
    def _gen_df(self, tickers, data):
        # Generate dataframe as tickers columns
        ans_df = pd.DataFrame()
        for tic in tickers:
            temp = pd.DataFrame([ele for ele in data if ele["ticker"] == tic])
            temp = temp[["Date","price"]].set_index("Date")
            temp = temp.rename(columns={"price":tic})
            ans_df = ans_df.join(temp, how="outer")
        ans_df = ans_df.fillna(method="backfill")
        return ans_df

