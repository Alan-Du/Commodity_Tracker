#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pandas as pd
import requests
import DB.fetch as fetch
import os
def dl_proc_params(start_date_str, end_date_str):
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
                date_list.append([int(date.strftime('%Y')),int(date.strftime('%m'))-1,int(date.strftime('%d')),date])
                i += 1
            return date_list
        else:
            print("input params end_date is earlier than start_date")
            raise
    else:
        return None


class DL_Inv_parser:
    def __init__( self ):
        self.PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.URL_TEMPL = "http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html"
        self.headers   = { 'Content-Type': 'application/x-www-form-urlencoded',
                           'Cookie': 'JSESSIONID=B2D36827C18F04E470A15A12B7C75AE5; WMONID=Zzot0IEoeuA; Hm_lvt_a50228174de2a93aee654389576b60fb=1569244935,1569337963,1569432080; Hm_lpvt_a50228174de2a93aee654389576b60fb=1569432127',
                           'Referer': 'http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
                         }
        self.payload = { 'wbillWeeklyQuotes.variety': 'all',
                         'year': 0,
                         'month':0,
                         'day':  0,
                       }
        self.col_names = ["Dates","Code","Open","High","Low","Close","OPI","Vol"]
        self.name_map  = {"豆一":"a","豆二":"b","乙二醇":"eg","焦煤":"jm","焦炭":"j",
                          "铁矿石":"i","聚氯乙烯":"pvc","聚丙烯":"pp","聚乙烯":"pe","豆粕":"m",
                          "豆油":"y","棕榈油":"p","鸡蛋":"jd","玉米淀粉":"cs","玉米":"c"}
        self.col_names = ["Product","Location","Y-D Inv","INV","Chg"]
        self.f_name    = self.PATH+"\\DL_INV_2019.xlsx" # Annually update herer
        self.datas     = []
    def download(self,sdate,edate):
        # Start downloading given period
        dates_li = dl_proc_params(sdate,edate)
        ans = pd.DataFrame()
        print("Exchange DL downloading...")
        for dates in dates_li:
            print(dates)
            self.payload['year'] = dates[0]
            self.payload['month'] = dates[1]
            self.payload['day'] = dates[2]
            page = requests.post( self.URL_TEMPL, data=self.payload, headers=self.headers).text
            try:
                df = pd.read_html(page,skiprows=1)[0]
            except:
                continue
            if df.shape[0] <= 2:
                continue
            df.columns = self.col_names
            df = df.fillna("NA")
            df = df[df["Product"].str.contains("小计")]
            df["Product"] = df["Product"].str.replace("小计", "")
            df = df.replace({"Product":self.name_map})[["Product","INV"]]
            df["Dates"] = dates[3]
            df = df[["Dates","Product","INV"]]
            ans = ans.append(df)
        self.datas = ans
        
    def weekly_update(self,sdate,edate):
        # Weekly update local DB
        self.download(sdate,edate)
        fetch.update_weekly_inventory(self.datas)
        return 0
        
    def get_data_df(self):
        return self.datas

###--- Testing ---###
#start_date = "2019-09-20"
#end_date   = "2019-09-25"
#DL = DL_Inv_parser()
#DL.weekly_update(start_date,end_date)