# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 10:33:22 2020
test program for commodity index update
@author: shaol
"""

import pandas as pd
import DB.fetch as fetch
from Analyzer import Ana_Helper as a_help
import stock_currency.stock_sector as SS
import stock_currency.industry_tracking as ind_tracking
import stock_currency.get_currency as GC
from datetime import datetime, timedelta
import Market.Market_Manager as market_mgm
import Market.MKT_Helper as helper
import matplotlib.pyplot as plt
import datetime as dt
product_name = ["ag","au","cu","al","zn","pb","ni","sn",
                "ZC","jm","j","i","rb","hc","FG",
                "TA","pvc","pp","pe","ru","bu","MA",
                "a","m","RM","y","OI","p","SR","CF","jd","cs","c",
                "IC","IF","IH","T","TF","TS",
                ]
product_name = ["AP"]
sdate = dt.datetime(2016,1,1).date()
cur_date = dt.datetime(2020,2,7).date()
fetch.upload_commodity_index(product_name,sdate,cur_date)

#product_name = ["AG","AU","CU","AL","ZN","PB","NI","SN",
#                "ZC","JM","J","I","RB","HC","FG",
#                "TA","PVC","PP","PE","RU","BU","MA",
#                "A","M","RM","Y","OI","P","SR","CF","JD","CS","C",
#                "IC","IF","IH","T","TF","TS",
#                ]
#N = 50
#index = pd.DataFrame(fetch.get_index_all())
#for name in product_name:
#    sec_data = index[index["name"] == name].set_index("Dates")
#    fig, axes = plt.subplots(nrows=2, ncols=1)
#    sec_data["close"].plot(ax=axes[0])
#    sec_data = sec_data.asfreq( freq = "W", how = "start", method = "ffill")
#    sec_data[["close"]].pct_change().rolling(window=N).skew().plot(ax=axes[1])
#

#cur_date = dt.datetime.today()
#sdate = dt.datetime(2015,1,1).date()

#fetch.upload_commodity_index(sdate,cur_date)
#product_name = ["AG","AU","CU","AL","ZN","PB","NI","SN",
#                "ZC","JM","J","I","RB","HC","FG",
#                "TA","PVC","PP","PE","RU","BU","MA",
#                "A","M","RM","Y","OI","P","SR","CF","JD","CS","C",
#                "IC","IF","IH","T","TF","TS",
#                ]
#data_index = pd.DataFrame(fetch.get_index_all()).set_index("Dates")
#prob_start = datetime(2015,12,31).date()
#probability = a_help.count_pos_prob(data_index,product_name,"M",prob_start)
#print(probability)


