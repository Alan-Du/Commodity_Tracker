#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import json
import requests
import datetime
import pandas as pd
import DB.fetch as fetch
import os
def check_proc_params(start_date_str, end_date_str):
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
                date_list.append([date.strftime("%Y"),date.strftime('%Y%m%d'),date])
                i += 1
            return date_list
        else:
            print("input params end_date is earlier than start_date")
            raise
    else:
        return None
    
class SH_Inv_parser:
    def __init__(self):
        self.PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.HEADER = [ 'Dates', 'Product', 'INV']
        self.URL_TEMPL = "http://www.shfe.com.cn/data/dailydata/{}weeklystock.dat"
        self.product_map = { "铜":"cu","铝":"al","锌":"zn","铅":"pb","镍":"ni","锡":"sn",
                             "天然橡胶":"ru","沥青(仓库)":"bu","螺纹钢":"rb","热轧卷板":"hc",
                             "黄金":"au","白银":"ag","原油":"sc"}
        self.f_name = self.PATH+"\\SH_INV_2019.xlsx" # Annually update herer
        self.datas = []
    def download( self,
                  start_date, end_date ):
        print("Exchange SH downloading...")
        date_list = check_proc_params(start_date, end_date)
        datas = []
        for date_str in date_list:
            print(date_str)
            url = self.URL_TEMPL.format(date_str[1])
            resp = requests.get(url)
            if resp.status_code == 404:
                continue
            elif resp.status_code != 200:
                print("the resp status code of date({}) is {}".format(date_str[0:2], resp.status_code))
            jsonObj = json.loads(resp.content.decode('utf-8'))
            for idx, l in enumerate(jsonObj['o_cursor']):
                # Pay attention to gold, silver and rb 
                # they have different format!!!
                if re.match(r'\S+?\$\$GOLD$', l['VARNAME']):
                    datas.append([date_str[2], l['VARNAME'].split('$$')[0],l['WRTWGHTS']])
                if re.match(r'\S+?\$\$SILVER$', l['VARNAME']) and re.match(r'\S+?\$\$Subtotal$', l['WHABBRNAME']):
                    datas.append([date_str[2], l['VARNAME'].split('$$')[0],l['WRTWGHTS']])
                if re.match(r'\S+?\$\$REBAR$', l['VARNAME']) and re.match(r'\S+?\$\$Total$', l['WHABBRNAME']):
                    datas.append([date_str[2], l['VARNAME'].split('$$')[0],l['WRTWGHTS']])
                if re.match(r'\S+?\$\$HOT ROLLED COILS$', l['VARNAME']) and re.match(r'\S+?\$\$Total$', l['WHABBRNAME']):
                    datas.append([date_str[2], l['VARNAME'].split('$$')[0],l['WRTWGHTS']])
                if not re.match(r'\S+?\$\$Total$', l['WHABBRNAME']):
                    continue
                datas.append([date_str[2], l['VARNAME'].split('$$')[0],l['SPOTWGHTS']])
        df = pd.DataFrame(datas)
        try:
            df.columns = self.HEADER
        except:
            df = pd.DataFrame(columns = self.HEADER)
        df = df.replace({"Product":self.product_map})
        self.datas = df
    
    def weekly_update(self,sdate,edate):
        # Weekly update local DB
        self.download(sdate,edate)
        fetch.update_weekly_inventory(self.datas)
        return 0

##--- Testing ---###
#start_date = "2019-09-20"
#end_date = "2019-09-21"
#SH_Inv = SH_Inv_parser()
#SH_Inv.weekly_update(start_date,end_date)