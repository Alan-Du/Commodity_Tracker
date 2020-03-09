# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 08:24:36 2019

@author: shaolun du
@contact: Shaolun.du@gmail.com

Structure outline:
"""

def ZJ_proc_params(start_date_str, end_date_str):
    import datetime,re
    def check_date_format(date_str):
        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            return True
        else:
            return False
    date_list = []
    if check_date_format(start_date_str) and \
        check_date_format(end_date_str):
        year_start, month_start, day_start = start_date_str.split("-")
        year_end, month_end, day_end = end_date_str.split("-")
        start_date = datetime.date(int(year_start),
                                   int(month_start),
                                   int(day_start))
        end_date = datetime.date(int(year_end),
                                 int(month_end),
                                 int(day_end))
        delta_days = (end_date-start_date).days
        i = 0
        if delta_days>=0:
            while i <= delta_days:
                date = start_date+datetime.timedelta(days=i)
                date_list.append([date.strftime('%Y%m'),date.strftime('%d')])
                i += 1
            return date_list
        else:
            print("input params end_date is earlier than start_date")
            raise
    else:
        return None

class ZJ_parser:
    def __init__( self ):
        self.URL_TEMPL = "http://www.cffex.com.cn/sj/hqsj/rtj/{}/{}/index.xml"
        self.headers   = ["Dates","Code","Open","High","Low","Close","OPI","Vol"]
        self.datas     = []
    def download(self,sdate,edate):
        print("Exchange ZJ--->")
        # Start downloading given period
        import pandas as pd
        import xml.etree.ElementTree as ET
        import requests
        df = pd.DataFrame(columns=self.headers)
        dates_li = ZJ_proc_params(sdate,edate)
        with requests.Session() as s:
            for dates in dates_li:
                print(dates)
                url = self.URL_TEMPL.format(dates[0],dates[1])
                page = s.get(url).text
                try:
                    etree = ET.fromstring(page)
                except:
                    continue
                for i in etree.iter(tag='dailydata'):
                    df = df.append(
                        pd.Series([ i.find('tradingday').text,i.find('instrumentid').text,
                                    i.find('openprice').text,i.find('highestprice').text,
                                    i.find('lowestprice').text,i.find('closeprice').text,
                                    i.find('openinterest').text,i.find('volume').text], index=self.headers),
                                    ignore_index=True)
        df = df.dropna()
        self.datas = df
    def get_data_df(self):
        return self.datas
#ZJ = ZJ_parser()
#ZJ.download("2019-01-02","2019-01-10")
#print(ZJ.get_data_df())
