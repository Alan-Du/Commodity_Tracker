# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 03:00:21 2020
Gold vs Silver combined with 10Y bond price
to check inflation or deflation
@author: shaolun du
@contact: shaolun.du@gmail.com
"""

import DB.dbFetch as dbFetch
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def gen_INF_spread(start,end):
    #generate bean and meal and oil comparison
    myFmt = mdates.DateFormatter('%y/%m') # Dates format
    Ticker_1  = "AU"
    Ticker_2  = "AG"
    Ticker_3  = "T"
    Ticker_4  = "CU"
    #Get raw market data
    index_data = pd.DataFrame(dbFetch.get_index_all()).set_index("Dates")
    inv_df = pd.DataFrame(dbFetch.get_historical_inventory()).set_index("Dates")
    
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
    Inventory = inv_df.loc[inv_df["Product"].str.upper()==Ticker_2][start:end]["INV"]
    market_2 = market_2.join(Inventory,how="left").fillna(0)
    
    market_3 = index_data[index_data["name"]==Ticker_3][start:end]
    market_3["T_price"] = 0.5*(market_3["open"]+market_3["close"])
    market_3["T_price"] = market_3["T_price"]/market_3["T_price"][0]
    market_3 = market_3[["T_price","r1"]]
    
    market_1 = market_1.join(market_3[["T_price"]],how="left").fillna(method="ffill")
    
    market_4 = index_data[index_data["name"]==Ticker_4][start:end]
    market_4["mid_price"] = 0.5*(market_4["open"]+market_4["close"])
    market_4["mid_price"] = market_4["mid_price"]/market_4["mid_price"][0]
    market_4 = market_4[["mid_price","r1"]]
    Inventory = inv_df.loc[inv_df["Product"].str.upper()==Ticker_4][start:end]["INV"]
    market_4 = market_4.join(Inventory,how="left").fillna(0)
    
    # Start plotting
    spread_name = Ticker_1+"_"+Ticker_2+"_Spread"
    fig, axes = plt.subplots(nrows=3, ncols=2,figsize=(10,12))    
    market_1[spread_name] = market_1["mid_price"]-market_2["mid_price"]
    axes[0,0].plot(market_1[spread_name],color='C0', label=Ticker_1+"-"+Ticker_2)
    ax2 = axes[0,0].twinx()
    ax2.plot(market_1["T_price"],color='C1', label="T_Bond")
    axes[0,0].legend()
    axes[0,0].xaxis.set_major_formatter(myFmt)
    axes[0,1].hist(market_1[spread_name],bins=50,color='C1', label=spread_name)
    axes[0,1].axvline(market_1[spread_name][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[0,1].get_ylim()
    pct_rank = market_1[spread_name].sort_values().values.searchsorted(market_1[spread_name][-1])/len(market_1[spread_name])
    axes[0,1].text(market_1[spread_name][-1], top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(market_1[spread_name][-1],pct_rank))
    
    spread_name = Ticker_1+"_"+Ticker_4+"_Spread"
    market_1[spread_name] = market_1["mid_price"]-market_4["mid_price"]
    axes[1,0].plot(market_1[spread_name],color='C0', label=Ticker_1+"-"+Ticker_4)
    ax2 = axes[1,0].twinx()
    ax2.plot(market_3["T_price"],color='C1', label="T_Bond")
    axes[1,0].legend()
    axes[1,0].xaxis.set_major_formatter(myFmt)
    axes[1,1].hist(market_1[spread_name],bins=50,color='C1', label=spread_name)
    axes[1,1].axvline(market_1[spread_name][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[1,1].get_ylim()
    pct_rank = market_1[spread_name].sort_values().values.searchsorted(market_1[spread_name][-1])/len(market_1[spread_name])
    axes[1,1].text(market_1[spread_name][-1], top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(market_1[spread_name][-1],pct_rank))
    
    spread_name = Ticker_2+"_"+Ticker_4+"_Spread"
    market_2[spread_name] = market_2["mid_price"]-market_4["mid_price"]
    axes[2,0].plot(market_2[spread_name],color='C0', label=Ticker_2+"-"+Ticker_4)
    ax2 = axes[2,0].twinx()
    ax2.plot(market_3["T_price"],color='C1', label="T_Bond")
    axes[2,0].legend()
    axes[2,0].xaxis.set_major_formatter(myFmt)
    axes[2,1].hist(market_2[spread_name],bins=50,color='C1', label=spread_name)
    axes[2,1].axvline(market_2[spread_name][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[2,1].get_ylim()
    pct_rank = market_2[spread_name].sort_values().values.searchsorted(market_2[spread_name][-1])/len(market_2[spread_name])
    axes[2,1].text(market_2[spread_name][-1], top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(market_2[spread_name][-1],pct_rank))
    
    fig.suptitle("Inflation Spread Strat",y=0.9)
    return fig