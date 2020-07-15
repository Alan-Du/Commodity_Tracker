#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import json
import requests
import pandas as pd
from Market.gen_process_params import gen_proc_params
from Market.exc_parser import exc_parser
class SH_inv_parser(exc_parser):
    def __init__(self):
        self.__contract_code = { "铜":"cu","铝":"al","锌":"zn","铅":"pb",
                                 "镍":"ni","锡":"sn","天然橡胶":"ru",
                                 "沥青仓库":"bu_warehouse","沥青厂库":"bu_factory",
                                 "螺纹钢":"rb","热轧卷板":"hc",
                                 "黄金":"au","白银":"ag","原油":"sc",
                                 "线材":"zl", "中质含硫原油":"sc",
                                 "燃料油":"fu","纸浆":"sp","20号胶":"nr",
                               }
        self.__exc_name = "SH_inv"
        self.__col_names = ['Dates', 'Product', 'INV']
        self.__datas = []
    def _get_URL_TEMP(self):
        # update exchange url
        URL_TEMPL = "http://www.shfe.com.cn/data/dailydata/{}dailystock.dat"
        return URL_TEMPL
    def _download(self, sdate,edate ):
        # Download market information from exchange
        print("Exchange SH inv downloading...")
        date_list = gen_proc_params(self.__exc_name,sdate,edate)
        datas = []
        for date_str in date_list:
            print(date_str)
            URL_TEMP = self._get_URL_TEMP()
            url = URL_TEMP.format(date_str[1])
            resp = requests.get(url)
            if resp.status_code == 404:
                continue
            elif resp.status_code != 200:
                print("the resp status code of date({}) is {}".format(date_str[0:2], resp.status_code))
            jsonObj = json.loads(resp.content.decode('utf-8'))
            datas = self._read_html_format(jsonObj, date_str, datas)
        df = pd.DataFrame(datas)
        try:
            df.columns = self.__col_names
        except:
            df = pd.DataFrame(columns = self.__col_names)
        # Over write to english product name
        df = df.replace({"Product":self.__contract_code})
        self.__datas = df
    def _read_html_format(self,jsonObj, date_str,datas):
        for idx, l in enumerate(jsonObj['o_cursor']):
            # Pay attention to gold with different format
            if re.match(r'\S+?\$\$GOLD$', l['VARNAME']):
                datas.append([date_str[2], l['VARNAME'].split('$$')[0],float(l['WRTWGHTS'])])
            if not re.match(r'\S+?\$\$Total$', l['WHABBRNAME']):
                continue
            datas.append([date_str[2], l['VARNAME'].split('$$')[0],float(l['WRTWGHTS'])])
        return datas
    def _get_data_df(self):
        self.__datas = self.__datas.dropna()
        self.__datas["Dates"] = pd.to_datetime(self.__datas["Dates"]).dt.date
        self.__datas = self.__datas.set_index("Dates")
        self.__datas["Product"] = self.__datas["Product"].astype(str)
        return self.__datas
