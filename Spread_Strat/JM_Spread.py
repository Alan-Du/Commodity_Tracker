# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 07:34:38 2020

@author: shaolun du
@contact: shaolun.du@gmail.com
"""

import DB.dbFetch as dbFetch
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def gen_JM_spread(start,end):
    #generate bean and meal and oil comparison
    myFmt = mdates.DateFormatter('%y/%m') # Dates format
    JM_Ticker  = "JM"
    J_Ticker  = "J"
    #Get raw market data
    index_data = pd.DataFrame(fetch.get_index_all()).set_index("Dates")
    inv_df = pd.DataFrame(fetch.get_historical_inventory()).set_index("Dates")
    
    JM_market = index_data[index_data["name"]==JM_Ticker][start:end]
    JM_market["mid_price"] = 0.5*(JM_market["open"]+JM_market["close"])
    JM_market["mid_price"] = JM_market["mid_price"]/JM_market["mid_price"][0]
    JM_market = JM_market[["mid_price","r1"]]
    Inventory = inv_df.loc[inv_df["Product"].str.upper()==JM_Ticker][start:end]["INV"]
    JM_market = JM_market.join( Inventory, how="left" ).fillna(0)
    
    
    J_market = index_data[index_data["name"]==J_Ticker][start:end]
    J_market["mid_price"] = 0.5*(J_market["open"]+J_market["close"])
    J_market["mid_price"] = J_market["mid_price"]/J_market["mid_price"][0]
    J_market = J_market[["mid_price","r1"]]
    Inventory = inv_df.loc[inv_df["Product"].str.upper()==J_Ticker][start:end]["INV"]
    J_market = J_market.join(Inventory,how="left").fillna(0)
    
    # Start plotting
    #Fig1: Bean and Bean Meal spread plot
    #Subplot 1,2: spread and spread distribution
    fig, axes = plt.subplots(nrows=5, ncols=2,figsize=(10,15))    
    JM_market["JM_J_Spread"] = JM_market["mid_price"]-J_market["mid_price"]
    axes[0,0].plot(JM_market["JM_J_Spread"],color='C0', label="JM-J")
    axes[0,0].legend()
    axes[0,1].hist(JM_market["JM_J_Spread"],bins=50,color='C1', label="JM_J_Spread")
    axes[0,1].axvline(JM_market["JM_J_Spread"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[0,1].get_ylim()
    pct_rank = JM_market["JM_J_Spread"].sort_values().values.searchsorted(JM_market["JM_J_Spread"][-1])/len(JM_market["JM_J_Spread"])
    axes[0,1].text(JM_market["JM_J_Spread"][-1], top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(JM_market["JM_J_Spread"][-1],pct_rank))
    
    #Subplot 3,4: single commodity price and roll yield
    axes[1,0].plot(JM_market["mid_price"],color='C0', label="JM")
    ax2 = axes[1,0].twinx()
    ax2.bar(JM_market.index,JM_market["r1"],alpha=0.5,width=3,color='C4', label="RollYield")
    axes[1,0].xaxis.set_major_formatter(myFmt)
    axes[1,0].legend()
    R1 = JM_market["r1"].dropna()
    pct_rank = R1.sort_values().values.searchsorted(R1[-1])/len(R1)
    axes[1,1].hist(R1,bins=50,color='C4',alpha=0.65)
    axes[1,1].axvline(R1[-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[1,1].get_ylim()
    axes[1,1].text(R1[-1]*1.1, top*0.9, 'Current:{:.0%},\nPct:{:.1%}'.format(R1[-1],pct_rank))
    
    axes[2,0].plot(J_market["mid_price"],color='C0', label="J")
    ax2 = axes[2,0].twinx()
    ax2.bar(J_market.index,J_market["r1"],alpha=0.5,width=3,color='C4', label="RollYield")
    axes[2,0].xaxis.set_major_formatter(myFmt)
    axes[2,0].legend()
    R1 = J_market["r1"].dropna()
    pct_rank = R1.sort_values().values.searchsorted(R1[-1])/len(R1)
    axes[2,1].hist(R1,bins=50,color='C4',alpha=0.65)
    axes[2,1].axvline(R1[-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[2,1].get_ylim()
    axes[2,1].text(R1[-1]*1.1, top*0.9, 'Current:{:.0%},\nPct:{:.1%}'.format(R1[-1],pct_rank))
    
    axes[3,0].bar(JM_market.index,JM_market["INV"],alpha=0.5,width=3,color='C4', label="JM_INV")
    axes[3,0].legend()
    pct_rank = JM_market["INV"].sort_values().values.searchsorted(JM_market["INV"][-1])/len(JM_market["INV"])
    axes[3,1].hist(JM_market["INV"],bins=50,color='C3',alpha=0.65)
    axes[3,1].axvline(JM_market["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[3,1].get_ylim()
    axes[3,1].text(JM_market["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}'.format(JM_market["INV"][-1],pct_rank))
    
    axes[4,0].bar(J_market.index,J_market["INV"],alpha=0.5,width=3,color='C4', label="J_INV")
    axes[4,0].legend()
    pct_rank = J_market["INV"].sort_values().values.searchsorted(J_market["INV"][-1])/len(J_market["INV"])
    axes[4,1].hist(J_market["INV"],bins=50,color='C3',alpha=0.65)
    axes[4,1].axvline(J_market["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[4,1].get_ylim()
    axes[4,1].text(J_market["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}'.format(J_market["INV"][-1],pct_rank))
    
    fig.suptitle('JM/J Spread Strat',y=0.9)
    return fig