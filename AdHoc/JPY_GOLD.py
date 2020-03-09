# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 12:04:55 2020
AdHoc project to get sense of JPY and Gold
@author: Shaolun Du
"""
import pandas as pd
import numpy as np
import DB.fetch as fetch
from Analyzer import Ana_Helper as a_help
import stock_currency.stock_sector as SS
import stock_currency.industry_tracking as ind_tracking
import stock_currency.get_currency as GC
from datetime import datetime, timedelta
import Market.Market_Manager as market_mgm
import matplotlib.pyplot as plt
from plotly.offline import plot
from plotly import graph_objs as go

end = datetime.today().date()- timedelta(days=1)
start = datetime(2016,1,1).date()
N = 700
data_index = pd.DataFrame(fetch.get_index_all())
comm = data_index[data_index["name"]=="AL"]
fig = go.Figure(data=[go.Candlestick(
                x=comm["Dates"],
                open=comm['open'],
                high=comm['high'],
                low=comm['low'],
                close=comm['close'])])

plot(fig)
#comm = comm.loc[end-timedelta(days=N):]
#comm["Mid_Price"] = (comm["close"]+comm["open"])/2
#comm["OPI_Chg"]   = comm["opi"].diff().fillna(0)
#
#min_p,max_p = min(comm["Mid_Price"]),max(comm["Mid_Price"])
#bins = 10
#leg = (max_p-min_p+2)/bins
#grouped = comm.groupby(pd.cut(comm["Mid_Price"], np.arange(min_p-1, max_p+1, leg))).sum().fillna(0)
#fig, axes = plt.subplots(nrows=1, ncols=1,figsize=(6,6))
#mean_idx = [(e.left+e.right)/2 for e in grouped.index.tolist()]
#axes = grouped["OPI_Chg"].plot.bar()
#axes.axvline(comm["Mid_Price"][-1], color='k', linestyle='dashed', linewidth=3)
#    
#print(comm["Mid_Price"][-1])
