#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import pandas as pd
from Market.exc_parser import exc_parser
from Market.gen_process_params import gen_proc_params
class DL_inv_parser(exc_parser):
    def __init__(self):
        self.__col_names = ["Product","Location","Y-D Inv","INV","Chg"]
        self.__exc_name  = "DL"
        self.__URL_TEMPL = "http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html"
        self.__headers   = { 'Content-Type': 'application/x-www-form-urlencoded',
                             'Cookie': 'JSESSIONID=B2D36827C18F04E470A15A12B7C75AE5; WMONID=Zzot0IEoeuA; Hm_lvt_a50228174de2a93aee654389576b60fb=1569244935,1569337963,1569432080; Hm_lpvt_a50228174de2a93aee654389576b60fb=1569432127',
                             'Referer': 'http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html',
                             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
                         }
        self.__payload  = { 'wbillWeeklyQuotes.variety': 'all',
                            'year': 0,
                            'month':0,
                            'day':  0,
                          }
        self.__name_map = {"豆一":"a","豆二":"b","乙二醇":"eg","焦煤":"jm","焦炭":"j",
                           "铁矿石":"i","聚氯乙烯":"pvc","聚丙烯":"pp","聚乙烯":"pe","豆粕":"m",
                           "豆油":"y","棕榈油":"p","鸡蛋":"jd","玉米淀粉":"cs","玉米":"c",
                          "苯乙烯":"eb","纤维板":"fb"}
        self.__datas     = []
    def _get_URL_TEMP(self):
        # update exchange url
        return self.__URL_TEMPL
    def _read_html_format(self,page,dates):
        df = pd.read_html(page,skiprows=0)[0]
        df.columns = self.__col_names
        df = df.fillna("NA")
        df = df[df["Product"].str.contains("小计")]
        df["Product"] = df["Product"].str.replace("小计", "")
        df = df.replace({"Product":self.__name_map})[["Product","INV"]]
        df["Dates"] = dates[3]
        df = df[["Dates","Product","INV"]]
        return df 
    def _download(self,sdate,edate):
        print("Exchange DL Inv--->")
        # Start downloading given period
        dates_li = gen_proc_params(self.__exc_name,sdate,edate)
        ans = pd.DataFrame()
        with requests.Session() as s:
            # Open request session
            for dates in dates_li:
                print(dates)
                self.__payload['year'] = dates[0]
                self.__payload['month'] = dates[1]
                self.__payload['day'] = dates[2]
                page = s.post( self.__URL_TEMPL, data=self.__payload, headers=self.__headers).text
                try:
                    df = self._read_html_format(page,dates)
                except:
                    continue
                ans = ans.append(df)
        self.__datas = ans
    def _get_data_df(self):
        # Convert output format
        self.__datas = self.__datas.dropna()
        self.__datas["Dates"] = pd.to_datetime(self.__datas["Dates"]).dt.date
        self.__datas = self.__datas.set_index("Dates")
        self.__datas["Product"] = self.__datas["Product"].astype(str)
        return self.__datas