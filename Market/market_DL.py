"""
Created on Sun Sep 22 08:24:36 2019

@author: shaolun du
@contact: Shaolun.du@gmail.com

Structure outline:
    HTML page with pandas read html parser
"""
import requests
import pandas as pd
from Market.exc_parser import exc_parser
from Market.gen_process_params import gen_proc_params
class DL_parser(exc_parser):
    """ Shanghai exchange parser
    """
    def __init__( self ):
        self.__col_names = ["Dates","Code","Open","High","Low","Close","OPI","Vol"]
        self.__exc_name  = "DL"
        self.__URL_TEMPL = "http://www.dce.com.cn/publicweb/quotesdata/dayQuotesCh.html"
        self.__headers   = { 'Content-Type': 'application/x-www-form-urlencoded',
                             'Cookie': 'JSESSIONID=34581314E8E6F047ABE7D22180DCE3A2; WMONID=-b8uBX4vHDi; Hm_lvt_a50228174de2a93aee654389576b60fb=1567732473,1568333912,1568936184,1569113640; Hm_lpvt_a50228174de2a93aee654389576b60fb=1569113660',
                             'Referer': 'http://www.dce.com.cn/publicweb/quotesdata/dayQuotesCh.html',
                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
                           }
        self.__payload  = { 'dayQuotes.variety': 'all',
                           'dayQuotes.trade_type': '0',
                           'year': 0,
                           'month':0,
                           'day':  0,
                         }
        self.__name_map = {"豆一":"a","豆二":"b","乙二醇":"eg","焦煤":"jm","焦炭":"j",
                           "铁矿石":"i","聚氯乙烯":"pvc","聚丙烯":"pp","聚乙烯":"pe","豆粕":"m",
                           "豆油":"y","棕榈油":"p","鸡蛋":"jd","玉米淀粉":"cs","玉米":"c"}
        self.__datas     = []
    def _get_URL_TEMP(self):
        # update exchange url
        return self.__URL_TEMPL
    def _read_html_format(self,page,dates):
        df = pd.read_html(page,skiprows=0)[0]
        df.iloc[:,0] = df.iloc[:,0].map(self.__name_map)
        df = df.dropna()
        df["Dates"] = str(dates[0])+"{:02d}".format(dates[1]+1)+"{:02d}".format(dates[2])
        df["Code"]  = df.iloc[:,0]+df.iloc[:,1].astype(int).astype(str)
        df["Open"]  = df.iloc[:,2]
        df["High"]  = df.iloc[:,3]
        df["Low"]   = df.iloc[:,4]
        df["Close"] = df.iloc[:,5]
        df["OPI"]   = df.iloc[:,11]
        df["Vol"]   = df.iloc[:,10]
        df = df[["Dates","Code","Open","High","Low","Close","OPI","Vol"]]
        return df 
    def _download(self,sdate,edate):
        print("Exchange DL--->")
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
        self.__datas["Code"] = self.__datas["Code"].astype(str)
        return self.__datas
