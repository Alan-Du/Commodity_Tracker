"""
Created on Sun Sep 22 08:24:36 2019

@author: shaolun du
@contact: Shaolun.du@gmail.com

Structure outline:
    HTML page with pandas read html parser
"""
import requests
import pandas as pd
from Market.gen_process_params import gen_proc_params
from Market.exc_parser import exc_parser
class ZZ_parser(exc_parser):
    """ Zhengzhou exchange parser
    """
    def __init__( self ):
        self.__col_names = ["Dates","Code","Open","High","Low","Close","OPI","Vol"]
        self.__exc_name = "ZZ"
        self.__datas     = []
    def _get_URL_TEMP(self, cur_Y):
        # update exchange url
        if cur_Y >= 2015:
            URL_TEMPL = "http://www.czce.com.cn/cn/DFSStaticFiles/Future/{}/{}/FutureDataDaily.htm"
        elif cur_Y < 2015:
            URL_TEMPL = "http://www.czce.com.cn/cn/exchange/{}/datadaily/{}.htm"
        else:
            print("Year not found.")
            raise
        return URL_TEMPL
    def _read_html_format(self, cur_Y, page):
        if cur_Y < 2018:
            # Minor table format changes since 2018
            df = pd.read_html(page,skiprows=1,attrs={"id":"senfe"})[0]
        else:
            df = pd.read_html(page,skiprows=0)[0]
        return df
    def _download(self,sdate,edate):
        print("Exchange ZZ--->")
        # Start downloading given period
        dates_li = gen_proc_params(self.__exc_name,sdate,edate)
        ans = pd.DataFrame()
        with requests.Session() as s:
            # Open request session
            for dates in dates_li:
                print(dates)
                URL_TEMPL = self._get_URL_TEMP(int(dates[0]))
                url = URL_TEMPL.format(dates[0],dates[1])
                try:
                    page = s.get(url).text
                    df = self._read_html_format(int(dates[0]),page)
                except:
                    continue
                df.columns = [i for i in range(14)]
                df["Dates"] = dates[1]
                df = df[["Dates",0,2,3,4,5,10,9]]
                df.columns = self.__col_names
                df = df.dropna()
                # Delete some non ASCII rows scrpped
                df = df[df["Code"].str.len()<=10]
                ans = ans.append(df)
        self.__datas = ans
    def _get_data_df(self):
        # Convert output format
        self.__datas["Dates"] = pd.to_datetime(self.__datas["Dates"]).dt.date
        self.__datas = self.__datas.set_index("Dates")
        self.__datas["Code"] = self.__datas["Code"].astype(str)
        self.__datas[["Open","High","Low","Close","OPI","Vol"]] = self.__datas[["Open","High","Low","Close","OPI","Vol"]].astype(float)
        return self.__datas
