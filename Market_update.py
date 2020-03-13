# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 14:06:04 2019
This script used for weekly market information update
related database is local DB login see DB.dbLogin
@author: Shaolun Du
@contact:Shaolun.du@gmail.com
"""
import Market.auto_dl as dl
import Market.auto_sh as sh
import Market.auto_zz as zz
import Market.auto_zj as zj
import Inventory.inventory_DL as Inv_DL
import Inventory.inventory_SH as Inv_SH
import Inventory.inventory_ZZ as Inv_ZZ
import DB.fetch as fetch
import datetime as dt
""" All products name listed below:
product_name = ["AG","AU",
                "CU","AL","ZN","PB","NI","SN",
                "ZC","JM","J","I","RB","HC","FG",
                "TA","PVC","PP","PE","RU","BU","MA",
                "A","M","RM","Y","OI","P","SR","CF","JD","CS","C",
                "IC","IF","IH","T","TF","TS",
                ]
"""
product_name = ["ag","au","cu","al","zn","pb","ni","sn",
                "ZC","jm","j","i","rb","hc","FG",
                "sc","TA","pvc","pp","pe","ru","bu","MA","eg","SA",
                "a","m","RM","y","OI","p","SR","CF","jd","cs","c","AP","UR",
                "IC","IF","IH","T","TF","TS",
                ]
N = 1 # Back looking download trading days
cur_date = dt.datetime.today()
sdate = cur_date - dt.timedelta(days=N)
""" Fetch currency information
"""
fetch.update_ccy_price(fetch.get_ccy_price(sdate,cur_date))

""" Update market information
"""
sdate = sdate.strftime('%Y-%m-%d')
edate = cur_date.strftime('%Y-%m-%d')

exc_parsers = [ dl.DL_parser(),
                zz.ZZ_parser(),
                zj.ZJ_parser(),
                sh.SH_parser() ]

for exc in exc_parsers:
    exc.download(sdate,edate)
    new_data = exc.get_data_df()
    fetch.update_weekly_commodity(new_data)
    
# Update commodity index database
fetch.upload_commodity_index(product_name,sdate,cur_date)

""" Update inventory information
"""
inv_parsers = [ Inv_SH.SH_Inv_parser(),
                Inv_ZZ.ZZ_Inv_parser(),
                Inv_DL.DL_Inv_parser() ]
for inv in inv_parsers:
    inv.weekly_update(sdate,edate)



