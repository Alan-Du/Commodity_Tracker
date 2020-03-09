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
import requests
import json
import re
def SH_proc_params(start_date_str, end_date_str):
    import re
    import datetime
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
                date_list.append(date.strftime('%Y%m%d'))
                i += 1
            return date_list
        else:
            print("input params end_date is earlier than start_date")
            raise
    else:
        return None

class SH_parser:
    def __init__( self ):
        self.URL_TEMPL = "http://www.shfe.com.cn/data/dailydata/{}.dat"
        self.headers   = ["Dates","Code","Open","High","Low","Close","OPI","Vol"]
        self.datas     = []
    def download(self,sdate,edate):
        print("Exchange SH--->")
        # Start downloading given period
        dates_li = SH_proc_params(sdate,edate)
        with requests.Session() as s:
            for dates in dates_li:
                print(dates)
                url = self.URL_TEMPL.format(dates)
                resp = s.get(url)
                try:
                    jsonObj = json.loads(resp.content.decode('utf-8'))
                except:
                    continue
                tradingday = dates
                for idx, l in enumerate(jsonObj['o_cursor']):
                    if not re.match(r'\S+\d\d\d\d', l['INSTRUMENTID']):
                        continue
                    self.datas.append([tradingday, l['INSTRUMENTID'].strip(),
                                      l['OPENPRICE'], l['HIGHESTPRICE'],
                                      l['LOWESTPRICE'], l['CLOSEPRICE'],
                                      l['OPENINTEREST'], l['VOLUME'] ])
    def get_data_df(self):
        import pandas as pd
        df = pd.DataFrame(self.datas)
        df.columns = self.headers
        return df