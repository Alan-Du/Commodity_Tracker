# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 23:39:46 2020
Script for Bean, Bean Meal and Bean OIL
@author: shaolun du
@contact: Shaolun.du@gmail.com
"""
import DB.dbFetch as dbFetch
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def gen_bean_spread(start,end):
    #generate bean and meal and oil comparison
    myFmt = mdates.DateFormatter('%y/%m') # Dates format
    B_Ticker = "A"
    M_Ticker = "M"
    Y_Ticker = "Y"
    #Get raw market data
    index_data = pd.DataFrame(dbFetch.get_index_all()).set_index("Dates")
    inv_df = pd.DataFrame(dbFetch.get_historical_inventory()).set_index("Dates")
    
    B_market = index_data[index_data["name"]==B_Ticker][start:end]
    B_market["mid_price"] = 0.5*(B_market["open"]+B_market["close"])
    B_market["mid_price"] = B_market["mid_price"]/B_market["mid_price"][0]
    B_market = B_market[["mid_price","r1"]]
    B_inventory = inv_df.loc[inv_df["Product"].str.upper()==B_Ticker][start:end]["INV"]
    B_market = B_market.join(B_inventory,how="left")
    
    M_market = index_data[index_data["name"]==M_Ticker][start:end]
    M_market["mid_price"] = 0.5*(M_market["open"]+M_market["close"])
    M_market["mid_price"] = M_market["mid_price"]/M_market["mid_price"][0]
    M_market = M_market[["mid_price","r1"]]
    M_inventory = inv_df.loc[inv_df["Product"].str.upper()==M_Ticker][start:end]["INV"]
    M_market = M_market.join(M_inventory,how="left")
    
    Y_market = index_data[index_data["name"]==Y_Ticker][start:end]
    Y_market["mid_price"] = 0.5*(Y_market["open"]+Y_market["close"])
    Y_market["mid_price"] = Y_market["mid_price"]/Y_market["mid_price"][0]
    Y_market = Y_market[["mid_price","r1"]]
    Y_inventory = inv_df.loc[inv_df["Product"].str.upper()==Y_Ticker][start:end]["INV"]
    Y_market = Y_market.join(Y_inventory,how="left")
    # Start plotting
    #Fig1: Bean and Bean Meal spread plot
    #Subplot 1-6: spread and spread distribution
    fig, axes = plt.subplots(nrows=9, ncols=2,figsize=(10,36))    
    B_market["B_M_Spread"] = B_market["mid_price"]-M_market["mid_price"]
    axes[0,0].plot(B_market["B_M_Spread"],color='C0', label="Bean-Meal")
    axes[0,0].legend()
    axes[0,1].hist(B_market["B_M_Spread"],bins=50,color='C1', label="B_M_Spread")
    axes[0,1].axvline(B_market["B_M_Spread"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[0,1].get_ylim()
    pct_rank = B_market["B_M_Spread"].sort_values().values.searchsorted(B_market["B_M_Spread"][-1])/len(B_market["B_M_Spread"])
    axes[0,1].text(B_market["B_M_Spread"][-1], top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(B_market["B_M_Spread"][-1],pct_rank))
    
    B_market["B_Y_Spread"] = B_market["mid_price"]-Y_market["mid_price"]
    axes[1,0].plot(B_market["B_Y_Spread"],color='C0', label="Bean-OIL")
    axes[1,0].legend()
    axes[1,1].hist(B_market["B_Y_Spread"],bins=50,color='C1', label="Spread")
    axes[1,1].axvline(B_market["B_Y_Spread"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[1,1].get_ylim()
    pct_rank = B_market["B_Y_Spread"].sort_values().values.searchsorted(B_market["B_Y_Spread"][-1])/len(B_market["B_Y_Spread"])
    axes[1,1].text(B_market["B_Y_Spread"][-1], top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(B_market["B_Y_Spread"][-1],pct_rank))
    
    M_market["M_Y_Spread"] = M_market["mid_price"]-Y_market["mid_price"]
    axes[2,0].plot(M_market["M_Y_Spread"],color='C0', label="Meal-OIL")
    axes[2,0].legend()
    axes[2,1].hist(M_market["M_Y_Spread"],bins=50,color='C1', label="Spread")
    axes[2,1].axvline(M_market["M_Y_Spread"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[2,1].get_ylim()
    pct_rank = M_market["M_Y_Spread"].sort_values().values.searchsorted(M_market["M_Y_Spread"][-1])/len(M_market["M_Y_Spread"])
    axes[2,1].text(M_market["M_Y_Spread"][-1], top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(M_market["M_Y_Spread"][-1],pct_rank))
    
    #Subplot 3,4: single commodity price and roll yield
    axes[3,0].plot(B_market["mid_price"],color='C0', label="Bean")
    ax2 = axes[3,0].twinx()
    ax2.bar(B_market.index,B_market["r1"],alpha=0.5,width=3,color='C4', label="RollYield")
    axes[3,0].xaxis.set_major_formatter(myFmt)
    axes[3,0].legend()
    R1 = B_market["r1"].dropna()
    pct_rank = R1.sort_values().values.searchsorted(R1[-1])/len(R1)
    axes[3,1].hist(R1,bins=50,color='C4',alpha=0.65)
    axes[3,1].axvline(R1[-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[3,1].get_ylim()
    axes[3,1].text(R1[-1]*1.1, top*0.9, 'Current:{:.0%},\nPct:{:.1%}'.format(R1[-1],pct_rank))
    
    axes[4,0].plot(M_market["mid_price"],color='C0', label="Bean Meal")
    ax2 = axes[4,0].twinx()
    ax2.bar(M_market.index,M_market["r1"],alpha=0.5,width=3,color='C4', label="RollYield")
    axes[4,0].xaxis.set_major_formatter(myFmt)
    axes[4,0].legend()
    R1 = M_market["r1"].dropna()
    pct_rank = R1.sort_values().values.searchsorted(R1[-1])/len(R1)
    axes[4,1].hist(R1,bins=50,color='C4',alpha=0.65)
    axes[4,1].axvline(R1[-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[4,1].get_ylim()
    axes[4,1].text(R1[-1]*1.1, top*0.9, 'Current:{:.0%},\nPct:{:.1%}'.format(R1[-1],pct_rank))
    
    axes[5,0].plot(Y_market["mid_price"],color='C0', label="Bean Oil")
    ax2 = axes[5,0].twinx()
    ax2.bar(Y_market.index,Y_market["r1"],alpha=0.5,width=3,color='C4', label="RollYield")
    axes[5,0].xaxis.set_major_formatter(myFmt)
    axes[5,0].legend()
    R1 = Y_market["r1"].dropna()
    pct_rank = R1.sort_values().values.searchsorted(R1[-1])/len(R1)
    axes[5,1].hist(R1,bins=50,color='C4',alpha=0.65)
    axes[5,1].axvline(R1[-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[5,1].get_ylim()
    axes[5,1].text(R1[-1]*1.1, top*0.9, 'Current:{:.0%},\nPct:{:.1%}'.format(R1[-1],pct_rank))
    
    axes[6,0].bar(B_market.index,B_market["INV"],alpha=0.5,width=3,color='C4', label="Bean_INV")
    axes[6,0].legend()
    pct_rank = B_market["INV"].sort_values().values.searchsorted(B_market["INV"][-1])/len(B_market["INV"])
    axes[6,1].hist(B_market["INV"],bins=50,color='C3',alpha=0.65)
    axes[6,1].axvline(B_market["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[6,1].get_ylim()
    axes[6,1].text(B_market["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}'.format(B_market["INV"][-1],pct_rank))
    
    axes[7,0].bar(M_market.index,M_market["INV"],alpha=0.5,width=3,color='C4', label="Meal_INV")
    axes[7,0].legend()
    pct_rank = M_market["INV"].sort_values().values.searchsorted(M_market["INV"][-1])/len(M_market["INV"])
    axes[7,1].hist(M_market["INV"],bins=50,color='C3',alpha=0.65)
    axes[7,1].axvline(M_market["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[7,1].get_ylim()
    axes[7,1].text(M_market["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}'.format(M_market["INV"][-1],pct_rank))
    
    axes[8,0].bar(Y_market.index,Y_market["INV"],alpha=0.5,width=3,color='C4', label="OIL_INV")
    axes[8,0].legend()
    pct_rank = Y_market["INV"].sort_values().values.searchsorted(Y_market["INV"][-1])/len(Y_market["INV"])
    axes[8,1].hist(Y_market["INV"],bins=50,color='C3',alpha=0.65)
    axes[8,1].axvline(Y_market["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[8,1].get_ylim()
    axes[8,1].text(Y_market["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}'.format(Y_market["INV"][-1],pct_rank))
    
    fig.suptitle('Bean/BeanMeal/BeanOIL Spread Strat',y=0.9)
    return fig

