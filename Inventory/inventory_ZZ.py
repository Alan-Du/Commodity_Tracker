#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import DB.fetch as fetch
import os
def check_proc_params(start_date_str, end_date_str):
    import re
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

class ZZ_Inv_parser:
    def __init__(self):
        self.PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.URL_TEMPL = "http://www.czce.com.cn/cn/DFSStaticFiles/Future/{}/{}/FutureDataWhsheet.htm"
        self.contract_code = { "白糖SR":"SR","一号棉CF":"CF",
                               "菜粕RM":"RM","菜籽油OI":"OI",
                               "PTA":"TA","甲醇MA":"MA",
                               "玻璃FG":"FG","动力煤ZC":"ZC"}
        self.f_name = self.PATH+"\\ZZ_INV_2019.xlsx" # Annually update herer
        self.datas = []
    def download(self,start_date, end_date):
        print("Exchange ZZ downloading...")
        date_list = check_proc_params(start_date, end_date)
        datas = []
        for date_str in date_list:
            print(date_str)
            url = self.URL_TEMPL.format(date_str[0],date_str[1])
            resp = requests.get(url)
            if resp.status_code == 404:
                continue
            elif resp.status_code != 200:
                print("the resp status code of date({}) is {}".format(date_str, resp.status_code))
            page = resp.content.decode('utf-8')
            soup = BeautifulSoup(page, 'html.parser')
            tables = soup.findAll("table")
            for table in tables:
                if int(date_str[0]) <= 2017 and table.b:
                    contract = table.b.get_text().split(u"单位")[0].strip().split(u"：")[-1]
                    idx = 0 # Column index for inventory
                    for tag in table.findAll("tr")[1].findAll("td"):
                        if u"仓单数量" in tag.get_text():
                            break
                        else:
                            idx += 1
                    if contract in self.contract_code.keys():
                        contract = self.contract_code[contract]
                        for row in table.findAll("tr"):
                            if row.findAll("td")[0].get_text() == u"总计":
                                try:
                                    invent = int(float(row.findAll("td")[idx].get_text()))
                                except:
                                    invent = 0
                                datas.append({"Product":contract,"Dates":date_str[2],"INV":invent})
                                break
                elif table.findParent("table") is None:
                    # After 2017 format
                    try:
                        contract = table.b.get_text().split(u"单位")[0].strip().split(u"：")[-1]
                    except:
                        continue
                    idx = 0 # Column index for inventory
                    for tag in table.findAll("tr")[1].findAll("td"):
                        if u"仓单数量" in tag.get_text():
                            break
                        else:
                            idx += 1
                    if contract in self.contract_code.keys():
                        contract = self.contract_code[contract]
                        for row in table.findAll("tr"):
                            if row.findAll("td")[0].get_text() == u"总计":
                                invent = int(float((row.findAll("td")[idx].get_text())))
                                datas.append({"Product":contract,"Dates":date_str[2],"INV":invent})
                                break
        df = pd.DataFrame(datas)
        self.datas = df
    def weekly_update(self,sdate,edate):
        # Weekly update local DB
        self.download(sdate,edate)
        fetch.update_weekly_inventory(self.datas)
        return 0
###--- Testing ---###
#start_date = "2019-12-01"
#end_date   = "2019-12-21"
#ZZ_Inv = ZZ_Inv_parser()
#ZZ_Inv.weekly_update(start_date,end_date)