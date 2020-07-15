# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 02:07:44 2020

@author: shaol
"""

import DB.dbFetch as dbFetch
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def gen_CA_spread(start,end):
    #generate bean and meal and oil comparison
    myFmt = mdates.DateFormatter('%y/%m') # Dates format
    Ticker_1 = "A"
    Ticker_2 = "C"
    #Get raw market data
    index_data = pd.DataFrame(dbFetch.get_index_all()).set_index("Dates")
    inv_df = pd.DataFrame(dbFetch.get_historical_inventory()).set_index("Dates")
    ccy_df = pd.DataFrame(dbFetch.get_histroical_ccy()).set_index("Dates")
    ccy_df = ccy_df[(ccy_df != 0).all(1)]["CNYUSD"]
    
    market_1 = index_data[index_data["name"]==Ticker_1][start:end]
    market_1["mid_price"] = 0.5*(market_1["open"]+market_1["close"])
    market_1["mid_price"] = market_1["mid_price"]/market_1["mid_price"][0]
    market_1 = market_1[["mid_price","r1"]]
    market_1 = market_1.join(ccy_df,how="left").fillna(method="ffill")
    
    inventory_1 = inv_df.loc[inv_df["Product"].str.upper()==Ticker_1][start:end]["INV"]
    market_1 = market_1.join(inventory_1,how="left")
    
    market_2 = index_data[index_data["name"]==Ticker_2][start:end]
    market_2["mid_price"] = 0.5*(market_2["open"]+market_2["close"])
    market_2["mid_price"] = market_2["mid_price"]/market_2["mid_price"][0]
    market_2 = market_2[["mid_price","r1"]]
    inventory_2 = inv_df.loc[inv_df["Product"].str.upper()==Ticker_2][start:end]["INV"]
    market_2 = market_2.join(inventory_2,how="left")
    
    # Start plotting
    #Fig1: Bean and Bean Meal spread plot
    #Subplot 1,2: spread and spread distribution
    spread_name = Ticker_1+"_"+Ticker_2+"_Spread"
    fig, axes = plt.subplots(nrows=5, ncols=2,figsize=(10,20))    
    market_1[spread_name] = market_1["mid_price"]-market_2["mid_price"]
    axes[0,0].plot(market_1[spread_name],color='C0', label=spread_name)
    axes[0,0].legend()
    axes[0,0].xaxis.set_major_formatter(myFmt)
    ax2 = axes[0,0].twinx()
    ax2.plot(market_1["CNYUSD"],color='C1', label="CNY")
    axes[0,1].hist(market_1[spread_name],bins=50,color='C1', label=spread_name)
    axes[0,1].axvline(market_1[spread_name][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[0,1].get_ylim()
    pct_rank = market_1[spread_name].sort_values().values.searchsorted(market_1[spread_name][-1])/len(market_1[spread_name])
    axes[0,1].text(market_1[spread_name][-1], top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(market_1[spread_name][-1],pct_rank))
    
    #Subplot 3,4: single commodity price and roll yield
    axes[1,0].plot(market_1["mid_price"],color='C0', label=Ticker_1)
    ax2 = axes[1,0].twinx()
    ax2.bar(market_1.index,market_1["r1"],alpha=0.5,width=3,color='C4', label="RollYield")
    axes[1,0].xaxis.set_major_formatter(myFmt)
    axes[1,0].legend()
    axes[1,0].xaxis.set_major_formatter(myFmt)
    R1 = market_2["r1"].dropna()
    pct_rank = R1.sort_values().values.searchsorted(R1[-1])/len(R1)
    axes[1,1].hist(R1,bins=50,color='C4',alpha=0.65)
    axes[1,1].axvline(R1[-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[1,1].get_ylim()
    axes[1,1].text(R1[-1]*1.1, top*0.9, 'Current:{:.0%},\nPct:{:.1%}'.format(R1[-1],pct_rank))
    
    axes[2,0].plot(market_2["mid_price"],color='C0', label=Ticker_2)
    ax2 = axes[2,0].twinx()
    ax2.bar(market_2.index,market_2["r1"],alpha=0.5,width=3,color='C4', label="RollYield")
    axes[2,0].xaxis.set_major_formatter(myFmt)
    axes[2,0].legend()
    axes[2,0].xaxis.set_major_formatter(myFmt)
    R1 = market_2["r1"].dropna()
    pct_rank = R1.sort_values().values.searchsorted(R1[-1])/len(R1)
    axes[2,1].hist(R1,bins=50,color='C4',alpha=0.65)
    axes[2,1].axvline(R1[-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[2,1].get_ylim()
    axes[2,1].text(R1[-1]*1.1, top*0.9, 'Current:{:.0%},\nPct:{:.1%}'.format(R1[-1],pct_rank))
    
    axes[3,0].bar(market_1.index,market_1["INV"],alpha=0.5,width=3,color='C4', label=Ticker_1+"_INV")
    axes[3,0].legend()
    axes[3,0].xaxis.set_major_formatter(myFmt)
    pct_rank = market_1["INV"].sort_values().values.searchsorted(market_1["INV"][-1])/len(market_1["INV"])
    axes[3,1].hist(market_1["INV"],bins=50,color='C3',alpha=0.65)
    axes[3,1].axvline(market_1["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[3,1].get_ylim()
    axes[3,1].text(market_1["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}'.format(market_1["INV"][-1],pct_rank))
    
    axes[4,0].bar(market_2.index,market_2["INV"],alpha=0.5,width=3,color='C4', label=Ticker_2+"_INV")
    axes[4,0].legend()
    axes[4,0].xaxis.set_major_formatter(myFmt)
    pct_rank = market_2["INV"].sort_values().values.searchsorted(market_2["INV"][-1])/len(market_2["INV"])
    axes[4,1].hist(market_2["INV"],bins=50,color='C3',alpha=0.65)
    axes[4,1].axvline(market_2["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[4,1].get_ylim()
    axes[4,1].text(market_2["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}'.format(market_2["INV"][-1],pct_rank))
    
    fig.suptitle(spread_name+' Strat',y=0.9)
    return fig