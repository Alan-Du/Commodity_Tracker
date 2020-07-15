#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import pandas as pd
from bs4 import BeautifulSoup
from Market.gen_process_params import gen_proc_params
from Market.exc_parser import exc_parser
class ZZ_inv_parser(exc_parser):
    def __init__(self):
        self.__contract_code = { "白糖SR":"SR", "一号棉CF":"CF",
                                 "菜粕RM":"RM", "菜籽油OI":"OI",
                                 "PTA":"TA",    "甲醇MA":"MA",
                                 "玻璃FG":"FG", "动力煤ZC":"ZC" }
        self.__exc_name = "ZZ"
        self.__datas = []
    def _download(self, sdate,edate ): 
        # Download market information from exchange
        print("Exchange ZZ downloading...")
        date_list = gen_proc_params(self.__exc_name, sdate, edate)
        datas = []
        for date_str in date_list:
            print(date_str)
            url_temp = self._get_URL_TEMP(int(date_str[0]))
            url = url_temp.format(date_str[0],date_str[1])
            resp = requests.get(url)
            if resp.status_code == 404:
                continue
            elif resp.status_code != 200:
                print("the resp status code of date({}) is {}".format(date_str, resp.status_code))
            page = resp.content.decode('utf-8')
            self._read_html_format(int(date_str[0]), page, datas, date_str[1])
        df = pd.DataFrame(datas)
        self.__datas = df
    def _get_URL_TEMP(self, cur_Y):
        # update exchange url
        if cur_Y > 2015:
            URL_TEMPL = "http://www.czce.com.cn/cn/DFSStaticFiles/Future/{}/{}/FutureDataWhsheet.htm"
        elif cur_Y <= 2015:
            URL_TEMPL = "http://www.czce.com.cn/cn/exchange/{}/datawhsheet/{}.htm"
        else:
            print("Year not found.")
            raise
        return URL_TEMPL
    def _read_html_format(self, cur_Y, page, datas, date_str):
        # Return data frame after read html
        soup = BeautifulSoup(page, 'html.parser')
        tables = soup.findAll("table")
        for table in tables:
            if cur_Y > 2017:
                # Format to get contract code changed since 2017
                try:
                    contract = table.b.get_text().split(u"单位")[0].strip().split(u"：")[-1]
                except:
                    continue
            elif cur_Y <= 2017 and table.b:
                contract = table.b.get_text().split(u"单位")[0].strip().split(u"：")[-1]
            idx = 0 # Column index for inventory
            for tag in table.findAll("tr")[1].findAll("td"):
                if u"仓单数量" in tag.get_text():
                    break
                else:
                    idx += 1
            if contract in self.__contract_code.keys():
                contract = self.__contract_code[contract]
                for row in table.findAll("tr"):
                    if row.findAll("td")[0].get_text() == u"总计":
                        loc_t = row.findAll("td")[idx]
                        if len(loc_t.findAll("td")) == 0:
                            invent = int(float((loc_t.get_text())))
                        else:
                            invent = int(float(loc_t.findAll("td")[0].get_text()))
                        datas.append({"Product":contract,"Dates":date_str,"INV":invent})
                        break
        return 0
    def _get_data_df(self):
        self.__datas = self.__datas.dropna()
        self.__datas["Dates"] = pd.to_datetime(self.__datas["Dates"]).dt.date
        self.__datas = self.__datas.set_index("Dates")
        self.__datas["Product"] = self.__datas["Product"].astype(str)
        return self.__datas