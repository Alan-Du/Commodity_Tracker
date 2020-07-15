# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 01:30:59 2020
Script for RM, and RM OIL
@author: shaolun du
@contact: Shaolun.du@gmail.com
"""

import DB.dbFetch as dbFetch
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def gen_RM_spread(start,end):
    #generate bean and meal and oil comparison
    myFmt = mdates.DateFormatter('%y/%m') # Dates format
    RM_Ticker = "RM"
    OI_Ticker = "OI"
    #Get raw market data
    index_data = pd.DataFrame(dbFetch.get_index_all()).set_index("Dates")
    inv_df = pd.DataFrame(dbFetch.get_historical_inventory()).set_index("Dates")
    
    RM_market = index_data[index_data["name"]==RM_Ticker][start:end]
    RM_market["mid_price"] = 0.5*(RM_market["open"]+RM_market["close"])
    RM_market["mid_price"] = RM_market["mid_price"]/RM_market["mid_price"][0]
    RM_market = RM_market[["mid_price","r1"]]
    B_inventory = inv_df.loc[inv_df["Product"].str.upper()==RM_Ticker][start:end]["INV"]
    RM_market = RM_market.join(B_inventory,how="left")
    
    OI_market = index_data[index_data["name"]==OI_Ticker][start:end]
    OI_market["mid_price"] = 0.5*(OI_market["open"]+OI_market["close"])
    OI_market["mid_price"] = OI_market["mid_price"]/OI_market["mid_price"][0]
    OI_market = OI_market[["mid_price","r1"]]
    M_inventory = inv_df.loc[inv_df["Product"].str.upper()==OI_Ticker][start:end]["INV"]
    OI_market = OI_market.join(M_inventory,how="left")
    
    # Start plotting
    #Fig1: Bean and Bean Meal spread plot
    #Subplot 1,2: spread and spread distribution
    fig, axes = plt.subplots(nrows=5, ncols=2,figsize=(10,20))    
    RM_market["RM_OIL_Spread"] = RM_market["mid_price"]-OI_market["mid_price"]
    axes[0,0].plot(RM_market["RM_OIL_Spread"],color='C0', label="RM-RMOIL")
    axes[0,0].legend()
    axes[0,0].xaxis.set_major_formatter(myFmt)
    axes[0,1].hist(RM_market["RM_OIL_Spread"],bins=50,color='C1', label="RM_OIL_Spread")
    axes[0,1].axvline(RM_market["RM_OIL_Spread"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[0,1].get_ylim()
    pct_rank = RM_market["RM_OIL_Spread"].sort_values().values.searchsorted(RM_market["RM_OIL_Spread"][-1])/len(RM_market["RM_OIL_Spread"])
    axes[0,1].text(RM_market["RM_OIL_Spread"][-1], top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(RM_market["RM_OIL_Spread"][-1],pct_rank))
    
    #Subplot 3,4: single commodity price and roll yield
    axes[1,0].plot(RM_market["mid_price"],color='C0', label="RM")
    ax2 = axes[1,0].twinx()
    ax2.bar(RM_market.index,RM_market["r1"],alpha=0.5,width=3,color='C4', label="RollYield")
    axes[1,0].xaxis.set_major_formatter(myFmt)
    axes[1,0].legend()
    axes[1,0].xaxis.set_major_formatter(myFmt)
    R1 = RM_market["r1"].dropna()
    pct_rank = R1.sort_values().values.searchsorted(R1[-1])/len(R1)
    axes[1,1].hist(R1,bins=50,color='C4',alpha=0.65)
    axes[1,1].axvline(R1[-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[1,1].get_ylim()
    axes[1,1].text(R1[-1]*1.1, top*0.9, 'Current:{:.0%},\nPct:{:.1%}'.format(R1[-1],pct_rank))
    
    axes[2,0].plot(OI_market["mid_price"],color='C0', label="RM OIL")
    ax2 = axes[2,0].twinx()
    ax2.bar(OI_market.index,OI_market["r1"],alpha=0.5,width=3,color='C4', label="RollYield")
    axes[2,0].xaxis.set_major_formatter(myFmt)
    axes[2,0].legend()
    axes[2,0].xaxis.set_major_formatter(myFmt)
    R1 = OI_market["r1"].dropna()
    pct_rank = R1.sort_values().values.searchsorted(R1[-1])/len(R1)
    axes[2,1].hist(R1,bins=50,color='C4',alpha=0.65)
    axes[2,1].axvline(R1[-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[2,1].get_ylim()
    axes[2,1].text(R1[-1]*1.1, top*0.9, 'Current:{:.0%},\nPct:{:.1%}'.format(R1[-1],pct_rank))
    
    axes[3,0].bar(RM_market.index,RM_market["INV"],alpha=0.5,width=3,color='C4', label="RM_INV")
    axes[3,0].legend()
    axes[3,0].xaxis.set_major_formatter(myFmt)
    pct_rank = RM_market["INV"].sort_values().values.searchsorted(RM_market["INV"][-1])/len(RM_market["INV"])
    axes[3,1].hist(RM_market["INV"],bins=50,color='C3',alpha=0.65)
    axes[3,1].axvline(RM_market["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[3,1].get_ylim()
    axes[3,1].text(RM_market["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}'.format(RM_market["INV"][-1],pct_rank))
    
    axes[4,0].bar(OI_market.index,OI_market["INV"],alpha=0.5,width=3,color='C4', label="OIL_INV")
    axes[4,0].legend()
    axes[4,0].xaxis.set_major_formatter(myFmt)
    pct_rank = OI_market["INV"].sort_values().values.searchsorted(OI_market["INV"][-1])/len(OI_market["INV"])
    axes[4,1].hist(OI_market["INV"],bins=50,color='C3',alpha=0.65)
    axes[4,1].axvline(OI_market["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[4,1].get_ylim()
    axes[4,1].text(OI_market["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}'.format(OI_market["INV"][-1],pct_rank))
    
    fig.suptitle('RMMeal/RMOIL Spread Strat',y=0.9)
    return fig