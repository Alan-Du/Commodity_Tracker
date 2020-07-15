# -*- coding: utf-8 -*-
"""
Created on Wed May 13 01:35:33 2020
Scripts to analyze L/S trend charecters of a commodity
@author: shaolun du
@contact: shaolun.du@gmail.com
"""
import DB.fetch as fetch

import pandas as pd 
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

myFmt = mdates.DateFormatter('%y/%m')
# Date format setting
start = dt.datetime(2013, 1, 1).date()
end = dt.date.today()
Save_df = False
Relative_Switch = True
N = 20
frequency = "D"
commodity_name = "CU"
# Commodity index data
index_data = pd.DataFrame(fetch.get_index_all()).set_index("Dates")
# Get market data
market = index_data[index_data["name"]==commodity_name][start:end]
market["VOL/OPI"] = market["volume"]/market["opi"]
market["mid_price"] = 0.5*(market["open"]+market["close"])
market = market[["mid_price","opi","volume","r1","r2","VOL/OPI"]]
market["r3"] = ((1+market["r1"])*(1+market["r2"])).pow(0.5)-1
start = min(market.index)

inv_df = pd.DataFrame(fetch.get_historical_inventory()).set_index("Dates")
inventory = inv_df.loc[inv_df["Product"].str.upper()==commodity_name][start:end]["INV"]
market = market.join(inventory,how="left")

R_mean = market["r1"].median()
market_short = market.loc[market['r1'] > R_mean]
market_long  = market.loc[market['r1'] < R_mean]

# Open a blank figure
fig, axes = plt.subplots(nrows=2, ncols=2,figsize=(12,10))
# Plot one: Market information
axes[0,0].plot(market["mid_price"],color='C0', label=commodity_name)
ax2 = axes[0,0].twinx()
ax2.bar(market_short.index,market_short["r3"],alpha=0.5,width=3,color='C4', label="RollYield")
axes[0,0].xaxis.set_major_formatter(myFmt)
ax2.legend()

axes[0,1].plot(market["mid_price"],color='C0', label=commodity_name)
ax2 = axes[0,1].twinx()
ax2.bar(market_long.index,market_long["r3"],alpha=0.5,width=3,color='C4', label="RollYield")
axes[0,1].xaxis.set_major_formatter(myFmt)
ax2.legend()

axes[1,0].plot(market["mid_price"],color='C0', label=commodity_name)
ax2 = axes[1,0].twinx()
ax2.bar(market_short.index,market_short["INV"],alpha=0.5,width=3,color='C4', label="INV")
axes[1,0].xaxis.set_major_formatter(myFmt)
ax2.legend()

axes[1,1].plot(market["mid_price"],color='C0', label=commodity_name)
ax2 = axes[1,1].twinx()
ax2.bar(market_long.index,market_long["INV"],alpha=0.5,width=3,color='C4', label="INV")
axes[1,1].xaxis.set_major_formatter(myFmt)
ax2.legend()

fig.autofmt_xdate()
plt.tight_layout()
plt.suptitle(commodity_name.upper()+"_Short/Long", fontsize=12,y=1.01)
plt.show()
plt.close(fig)

