# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 08:24:36 2019

@author: shaolun du
@contact: Shaolun.du@gmail.com

Structure outline:
"""
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from Market.exc_parser import exc_parser
from Market.gen_process_params import gen_proc_params
class ZJ_parser(exc_parser):
    """ Shanghai exchange parser
    """
    def __init__( self ):
        self.__URL_TEMPL = "http://www.cffex.com.cn/sj/hqsj/rtj/{}/{}/index.xml"
        self.__headers   = ["Dates","Code","Open","High","Low","Close","OPI","Vol"]
        self.__exc_name  = "ZJ"
        self.__datas     = []
    def _get_URL_TEMP(self):
        # update exchange url
        return self.__URL_TEMPL
    def _read_html_format(self,page, df):
        etree = ET.fromstring(page)
        for i in etree.iter(tag='dailydata'):
            df = df.append(
                pd.Series([ i.find('tradingday').text,i.find('instrumentid').text,
                            i.find('openprice').text,i.find('highestprice').text,
                            i.find('lowestprice').text,i.find('closeprice').text,
                            i.find('openinterest').text,i.find('volume').text], index=self.__headers),
                            ignore_index=True)
        return df 
    def _download(self,sdate,edate):
        print("Exchange ZJ--->")
        # Start downloading given period
        df = pd.DataFrame(columns=self.__headers)
        dates_li = gen_proc_params(self.__exc_name,sdate,edate)
        with requests.Session() as s:
            for dates in dates_li:
                print(dates)
                url = self.__URL_TEMPL.format(dates[0],dates[1])
                page = s.get(url).text
                try:
                    df = self._read_html_format(page, df)
                except:
                    continue
        self.__datas = df
    def _get_data_df(self):
        # Convert output format
        self.__datas = self.__datas.dropna()
        self.__datas["Dates"] = pd.to_datetime(self.__datas["Dates"]).dt.date
        self.__datas = self.__datas.set_index("Dates")
        self.__datas["Code"] = self.__datas["Code"].astype(str)
        return self.__datas