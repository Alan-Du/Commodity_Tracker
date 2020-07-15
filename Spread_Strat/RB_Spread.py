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

def gen_RB_spread(start,end):
    #generate bean and meal and oil comparison
    myFmt = mdates.DateFormatter('%y/%m') # Dates format
    RB_Ticker = "RB"
    I_Ticker  = "I"
    J_Ticker  = "J"
    #Get raw market data
    index_data = pd.DataFrame(dbFetch.get_index_all()).set_index("Dates")
    inv_df = pd.DataFrame(dbFetch.get_historical_inventory()).set_index("Dates")
    
    RB_market = index_data[index_data["name"]==RB_Ticker][start:end]
    RB_market["mid_price"] = 0.5*(RB_market["open"]+RB_market["close"])
    RB_market["mid_price"] = RB_market["mid_price"]/RB_market["mid_price"][0]
    RB_market = RB_market[["mid_price","r1"]]
    Inventory = inv_df.loc[inv_df["Product"].str.upper()==RB_Ticker][start:end]["INV"]
    RB_market = RB_market.join( Inventory, how="left" ).fillna(0)
    
    I_market = index_data[index_data["name"]==I_Ticker][start:end]
    I_market["mid_price"] = 0.5*(I_market["open"]+I_market["close"])
    I_market["mid_price"] = I_market["mid_price"]/I_market["mid_price"][0]
    I_market = I_market[["mid_price","r1"]]
    Inventory = inv_df.loc[inv_df["Product"].str.upper()==I_Ticker][start:end]["INV"]
    I_market = I_market.join(Inventory,how="left").fillna(0)
    
    J_market = index_data[index_data["name"]==J_Ticker][start:end]
    J_market["mid_price"] = 0.5*(J_market["open"]+J_market["close"])
    J_market["mid_price"] = J_market["mid_price"]/J_market["mid_price"][0]
    J_market = J_market[["mid_price","r1"]]
    Inventory = inv_df.loc[inv_df["Product"].str.upper()==J_Ticker][start:end]["INV"]
    J_market = J_market.join(Inventory,how="left").fillna(0)
    
    # Start plotting
    #Fig1: Bean and Bean Meal spread plot
    #Subplot 1,2: spread and spread distribution
    fig, axes = plt.subplots(nrows=8, ncols=2,figsize=(10,20))    
    RB_market["RB_I_Spread"] = RB_market["mid_price"]-I_market["mid_price"]
    axes[0,0].plot(RB_market["RB_I_Spread"],color='C0', label="RB-I")
    axes[0,0].legend()
    axes[0,0].xaxis.set_major_formatter(myFmt)
    axes[0,1].hist(RB_market["RB_I_Spread"],bins=50,color='C1', label="RB_I_Spread")
    axes[0,1].axvline(RB_market["RB_I_Spread"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[0,1].get_ylim()
    pct_rank = RB_market["RB_I_Spread"].sort_values().values.searchsorted(RB_market["RB_I_Spread"][-1])/len(RB_market["RB_I_Spread"])
    axes[0,1].text(RB_market["RB_I_Spread"][-1], top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(RB_market["RB_I_Spread"][-1],pct_rank))
    
    RB_market["RB_J_Spread"] = RB_market["mid_price"]-J_market["mid_price"]
    axes[1,0].plot(RB_market["RB_J_Spread"],color='C0', label="RB-J")
    axes[1,0].legend()
    axes[1,0].xaxis.set_major_formatter(myFmt)
    axes[1,1].hist(RB_market["RB_J_Spread"],bins=50,color='C1', label="RB_J_Spread")
    axes[1,1].axvline(RB_market["RB_J_Spread"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[1,1].get_ylim()
    pct_rank = RB_market["RB_J_Spread"].sort_values().values.searchsorted(RB_market["RB_J_Spread"][-1])/len(RB_market["RB_J_Spread"])
    axes[1,1].text(RB_market["RB_J_Spread"][-1], top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(RB_market["RB_J_Spread"][-1],pct_rank))
    
    #Subplot 3,4: single commodity price and roll yield
    axes[2,0].plot(RB_market["mid_price"],color='C0', label="RB")
    ax2 = axes[2,0].twinx()
    ax2.bar(RB_market.index,RB_market["r1"],alpha=0.5,width=3,color='C4', label="RollYield")
    axes[2,0].xaxis.set_major_formatter(myFmt)
    axes[2,0].legend()
    axes[2,0].xaxis.set_major_formatter(myFmt)
    R1 = RB_market["r1"].dropna()
    pct_rank = R1.sort_values().values.searchsorted(R1[-1])/len(R1)
    axes[2,1].hist(R1,bins=50,color='C4',alpha=0.65)
    axes[2,1].axvline(R1[-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[2,1].get_ylim()
    axes[2,1].text(R1[-1]*1.1, top*0.9, 'Current:{:.0%},\nPct:{:.1%}'.format(R1[-1],pct_rank))
    
    axes[3,0].plot(I_market["mid_price"],color='C0', label="IRON")
    ax2 = axes[3,0].twinx()
    ax2.bar(I_market.index,I_market["r1"],alpha=0.5,width=3,color='C4', label="RollYield")
    axes[3,0].xaxis.set_major_formatter(myFmt)
    axes[3,0].legend()
    axes[3,0].xaxis.set_major_formatter(myFmt)
    R1 = I_market["r1"].dropna()
    pct_rank = R1.sort_values().values.searchsorted(R1[-1])/len(R1)
    axes[3,1].hist(R1,bins=50,color='C4',alpha=0.65)
    axes[3,1].axvline(R1[-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[3,1].get_ylim()
    axes[3,1].text(R1[-1]*1.1, top*0.9, 'Current:{:.0%},\nPct:{:.1%}'.format(R1[-1],pct_rank))
    
    axes[4,0].plot(J_market["mid_price"],color='C0', label="J")
    ax2 = axes[4,0].twinx()
    ax2.bar(J_market.index,J_market["r1"],alpha=0.5,width=3,color='C4', label="RollYield")
    axes[4,0].xaxis.set_major_formatter(myFmt)
    axes[4,0].legend()
    axes[4,0].xaxis.set_major_formatter(myFmt)
    R1 = J_market["r1"].dropna()
    pct_rank = R1.sort_values().values.searchsorted(R1[-1])/len(R1)
    axes[4,1].hist(R1,bins=50,color='C4',alpha=0.65)
    axes[4,1].axvline(R1[-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[4,1].get_ylim()
    axes[4,1].text(R1[-1]*1.1, top*0.9, 'Current:{:.0%},\nPct:{:.1%}'.format(R1[-1],pct_rank))
    
    axes[5,0].bar(RB_market.index,RB_market["INV"],alpha=0.5,width=3,color='C4', label="RB_INV")
    axes[5,0].legend()
    axes[5,0].xaxis.set_major_formatter(myFmt)
    pct_rank = RB_market["INV"].sort_values().values.searchsorted(RB_market["INV"][-1])/len(RB_market["INV"])
    axes[5,1].hist(RB_market["INV"],bins=50,color='C3',alpha=0.65)
    axes[5,1].axvline(RB_market["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[5,1].get_ylim()
    axes[5,1].text(RB_market["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}'.format(RB_market["INV"][-1],pct_rank))
    
    axes[6,0].bar(I_market.index,I_market["INV"],alpha=0.5,width=3,color='C4', label="I_INV")
    axes[6,0].legend()
    axes[6,0].xaxis.set_major_formatter(myFmt)
    pct_rank = I_market["INV"].sort_values().values.searchsorted(I_market["INV"][-1])/len(I_market["INV"])
    axes[6,1].hist(I_market["INV"],bins=50,color='C3',alpha=0.65)
    axes[6,1].axvline(I_market["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[6,1].get_ylim()
    axes[6,1].text(I_market["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}'.format(I_market["INV"][-1],pct_rank))
    
    axes[7,0].bar(J_market.index,J_market["INV"],alpha=0.5,width=3,color='C4', label="J_INV")
    axes[7,0].legend()
    axes[7,0].xaxis.set_major_formatter(myFmt)
    pct_rank = J_market["INV"].sort_values().values.searchsorted(J_market["INV"][-1])/len(J_market["INV"])
    axes[7,1].hist(J_market["INV"],bins=50,color='C3',alpha=0.65)
    axes[7,1].axvline(J_market["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[7,1].get_ylim()
    axes[7,1].text(J_market["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}'.format(J_market["INV"][-1],pct_rank))
    
    fig.suptitle('RB/I/J Spread Strat',y=0.9)
    return fig