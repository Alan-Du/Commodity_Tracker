# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 03:00:21 2020
Gold vs Silver combined with 10Y bond price
to check inflation or deflation
@author: shaolun du
@contact: shaolun.du@gmail.com
"""

import DB.fetch as fetch
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def gen_CCY_spread(Ticker_1,i_start,i_end):
    #generate bean and meal and oil comparison
    myFmt = mdates.DateFormatter('%y/%m') # Dates format
#    Ticker_1  = "TA"
    Ticker_2  = "T"    #Get raw market data
    index_data = pd.DataFrame(fetch.get_index_all()).set_index("Dates")
    currency   = pd.DataFrame(fetch.get_histroical_ccy()).set_index("Dates")
    inv_df     = pd.DataFrame(fetch.get_historical_inventory()).set_index("Dates")
    
    market_1 = index_data[index_data["name"]==Ticker_1][start:end]
    market_1["mid_price"] = 0.5*(market_1["open"]+market_1["close"])
    market_1["mid_price"] = market_1["mid_price"]/market_1["mid_price"][0]
    market_1 = market_1[["mid_price","r1"]]
    Inventory = inv_df.loc[inv_df["Product"].str.upper()==Ticker_1][start:end]["INV"]
    market_1 = market_1.join( Inventory, how="left" ).fillna(0)
    
    market_2 = index_data[index_data["name"]==Ticker_2][start:end]
    market_2["mid_price"] = 0.5*(market_2["open"]+market_2["close"])
    market_2["mid_price"] = market_2["mid_price"]/market_2["mid_price"][0]
    market_2 = market_2[["mid_price","r1"]]
    
    CNY = currency[["CNYUSD"]][start:end]
    CNY = CNY/CNY.iloc[0]
    OIL = currency[["WTI"]][start:end]
    OIL = OIL/OIL.iloc[0]
    market_1 = market_1.join( CNY, how="left" ).fillna(method = "ffill")
    market_1 = market_1.join( OIL, how="left" ).fillna(method = "ffill")
    # Start plotting
    fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(10,6))
    axes[0].plot(market_1["mid_price"],color='C0', label=Ticker_1)
    ax2 = axes[0].twinx()
    ax2.plot(market_1["WTI"]+market_1["CNYUSD"],color='C1', label="OIL+CNY")
    ax2.legend()
    axes[0].xaxis.set_major_formatter(myFmt)
    axes[1].plot(market_2["mid_price"]-market_1["CNYUSD"],color='C0', label="T_Bond-CCY")
    ax2 = axes[1].twinx()
    ax2.plot(market_1["mid_price"],color='C1', label=Ticker_1)
    axes[1].legend()
    axes[1].xaxis.set_major_formatter(myFmt)
    
    fig.suptitle("Currency Spread Strat",y=0.95)
    
    return fig

start = dt.datetime(2013, 1, 1).date()
end = dt.date.today()
gen_CCY_spread("TA",start,end)