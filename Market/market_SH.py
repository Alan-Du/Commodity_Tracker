# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 08:24:36 2019

@author: shaolun du
@contact: Shaolun.du@gmail.com

Structure outline:
{'PRODUCT': 'sc', 'PRODUCTSORTNO': 90, 'ORDERNO': 1, 
'INSTRUMENTID': 'sc2012', 'OPENPRICE': 457, 'HIGHESTPRICE': 461, 
'LOWESTPRICE': 452.1, 'CLOSEPRICE': 441.8, 'PRICECHG': 18.6, 
'OPENINTEREST': 54, 'OPENINTERESTCHG': 2, 'SETTLEMENTPRICE': 441.8, 
'VOLUME': 18, 'TURNOVER': 821.58, 'PRODUCTID': 'sc_f', 'ORDERNO2': 0}
"""
import re
import json
import requests
import pandas as pd
from Market.gen_process_params import gen_proc_params
from Market.exc_parser import exc_parser
class SH_parser(exc_parser):
    """ Shanghai exchange parser
    """
    def __init__( self ):
        self.__col_names = ["Dates","Code","Open","High","Low","Close","OPI","Vol"]
        self.__exc_name  = "SH"
        self.__datas     = []
    def _get_URL_TEMP(self):
        # update exchange url
        URL_TEMPL = "http://www.shfe.com.cn/data/dailydata/{}.dat"
        return URL_TEMPL
    def _read_html_format(self,dates, jsonObj, temp_ans):
        tradingday = dates
        for idx, l in enumerate(jsonObj['o_cursor']):
            if not re.match(r'\S+\d\d\d\d', l['INSTRUMENTID']):
                continue
            try:
                temp_ans.append([ tradingday, l['INSTRUMENTID'].strip(),
                                  float(l['OPENPRICE']), float(l['HIGHESTPRICE']),
                                  float(l['LOWESTPRICE']), float(l['CLOSEPRICE']),
                                  float(l['OPENINTEREST']), float(l['VOLUME']) ])
            except:
                continue
        return temp_ans
    def _download(self,sdate,edate):
        print("Exchange SH--->")
        # Start downloading given period
        dates_li = gen_proc_params(self.__exc_name,sdate,edate)
        temp_ans = []
        with requests.Session() as s:
            # Open request session
            for dates in dates_li:
                print(dates)
                URL_TEMPL = self._get_URL_TEMP()
                url = URL_TEMPL.format(dates)
                resp = s.get(url)
                jsonObj = json.loads(resp.content.decode('utf-8'))
                temp_ans = self._read_html_format(dates, jsonObj, temp_ans)
        self.__datas = pd.DataFrame(temp_ans)
        self.__datas.columns = self.__col_names
    def _get_data_df(self):
        # Convert output format
        self.__datas = self.__datas.dropna()
        self.__datas["Dates"] = pd.to_datetime(self.__datas["Dates"]).dt.date
        self.__datas = self.__datas.set_index("Dates")
        self.__datas["Code"] = self.__datas["Code"].astype(str)
        return self.__datas