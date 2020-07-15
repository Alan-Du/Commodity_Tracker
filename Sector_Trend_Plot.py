# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 21:53:15 2020
Tracking and plot commodity sector movements
basic logic is if the whole sector move in the 
same direction that shows a strong signal of 
sector trend
@author: shaolun du
@contact: shaolun.du@gmail.com
"""
import numpy as np
import pandas as pd
import datetime as dt
import DB.fetch as fetch
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Tracker_Central_Dict import Sector_Commodity_Dict as Sec_Dict

Sectors_Dict = Sec_Dict.sector_comm_dict
Sector_Score = pd.DataFrame()
# Date format setting
pd.options.mode.chained_assignment = None  # default='warn'
end   = dt.date.today()-dt.timedelta(days = 1)
start = end - dt.timedelta(days = 60)
# Data Preparition
index_data = pd.DataFrame(fetch.get_index_all()).set_index("Dates")[start:end]
for name,secs in Sectors_Dict.items():
    total_N = len(secs)
    temp_df = pd.DataFrame()
    for commodity_name in secs:
        market = index_data[index_data["name"]==commodity_name]
        market["mid_price"] = 0.5*(market["open"]+market["close"])
        market["rets"] = market["mid_price"].diff()
        market["OPI_chg"] = market["opi"].diff()
        market[commodity_name] = np.where((market["rets"]>0)&(market["OPI_chg"]>0),1, np.where((market["rets"])<0&(market["OPI_chg"]>0),-1,0))
        if len(temp_df) == 0:
            temp_df = market[[commodity_name]]
        else:
            temp_df = temp_df.join(market[commodity_name],how="outer")
    temp_df = temp_df.fillna(method='ffill')
    temp_df[name] = temp_df.sum(axis=1)/len(secs)
    if len(Sector_Score) == 0:
        Sector_Score = temp_df[[name]]
    else:
        Sector_Score = Sector_Score.join(temp_df[name],how="outer")
    Sector_Score = Sector_Score.fillna(method='ffill')

myFmt = mdates.DateFormatter('%y/%m')
# Open a blank figure
fig, axes = plt.subplots(nrows=3, ncols=2,figsize=(10,8))
i,j=0,0
for name,ss in Sectors_Dict.items():
    if j == 2:
        j = 0
        i += 1
    if i > 2:
        break
    axes[i,j].hist(Sector_Score[name],bins=50,label=name)
    axes[i,j].axvline(Sector_Score[name][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[i,j].get_ylim()
    axes[i,j].text(Sector_Score[name][-1]*1.1, top*0.9, 'Date:{:%m/%d},\nCurrent:{:.1}'.format(Sector_Score[name].index[-1],Sector_Score[name][-1]))
    axes[i,j].legend()
    j += 1
plt.tight_layout()
plt.suptitle("Sector_Scores", fontsize=10,y=1.01)
plt.show()
plt.close(fig)

        