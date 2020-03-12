# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 10:18:38 2020
Single commodity analyzer scripts
@author: Shaolun Du
@contacts: Shaolun.du@gmail.com
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def cal_responce_tb(market,stock_name,responce_start):
    # column names = "mid_price","opi","volume","r1"
    #               "VOL/OPI","bond_price","XX_Stock",
    #               "USD_Index","CNYUSD","JPYUSD","WTI"
    # Using 2.33 std represents for 95% probability 1D
    ans_bk = []
    pct_market = market.pct_change()*100
    for target in ["bond_price",stock_name+"_Stock","USD_Index","CNYUSD","JPYUSD","WTI"]:
        std_95 = pct_market[target].std()*1.65
        temp = pct_market[["mid_price",target]].loc[abs(pct_market[target])>=std_95]
        temp = temp.loc[responce_start:]
        ans_bk += [{"Dates":ele[0],"price_chg":ele[1],"driver_chg":ele[2],"driver":target,"Responce_Ratio":ele[1]/ele[2]} for ele in temp.to_records()]
    return pd.DataFrame(ans_bk)[["Dates","price_chg","driver","driver_chg","Responce_Ratio"]]
def cal_stat_analyze(market,stock_name):
    # Calculate statistics 
    frequency = "M"
    market = market.rename(columns={"mid_price": stock_name})
    columns_name = [ stock_name,stock_name+"_Stock","INV",
                     "bond_price","WTI",
                     "USD_Index","CNYUSD","JPYUSD"]
    day_rng = pd.date_range(market.index[0], market.index[-1], freq='D', closed='left')
    market = market.reindex(day_rng, method='ffill')
    market = market[columns_name].asfreq(freq=frequency).pct_change()
    market["Month"] = market.index.month
    grouped = market.groupby(['Month'])[columns_name].apply(lambda x:(x>0).sum()/x.count())
    grouped = grouped.round(2).T
    return grouped

def single_stock_analyze( comm_name, stock_name, market, N ):
    # Generate single commodity report
    # Inputs: comm_name, stock_name, market_df(generated from retirever)
    # Outputs: market plot, roll_yield plot, inventory plot,
    #          stock plot, correlation to Oil, 10Y bond, 
    #                      CNYUSD, JPYUSD, USD index plots
    #          monthly up probability matrix, 
    myFmt = mdates.DateFormatter('%y/%m')
    # Open a blank figure
    fig, axes = plt.subplots(nrows=9, ncols=2,figsize=(12,30))
    # Plot one: Market information
    axes[0,0].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[0,0].twinx()
    ax2.bar(market.index,market["volume"],alpha=0.5,width=3,color='C1', label="Volume")
    ax2.plot(market["opi"],color='C2',alpha=0.5, label="OPI")
    axes[0,0].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    # Hist three: VOl/OPI
    pct_rank = market["VOL/OPI"].sort_values().values.searchsorted(market["VOL/OPI"][-1])/len(market["VOL/OPI"])
    axes[0,1].hist(market["VOL/OPI"],bins=50,color='C0', label="VOL/OPI")
    axes[0,1].axvline(market["VOL/OPI"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[0,1].get_ylim()
    axes[0,1].text(market["VOL/OPI"][-1]*1.1, top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(market["VOL/OPI"][-1],pct_rank))
    # Plot two: Market structure (RYs)
    axes[1,0].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[1,0].twinx()
    ax2.bar(market.index,market["r1"],alpha=0.5,width=3,color='C4', label="RollYield")
    ax2.plot(market["r1"].rolling(window = 50).std(),color='C2', alpha=0.5, label="std(RY)")
    axes[1,0].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    # Plot three: Stock compare
    axes[3,0].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[3,0].twinx()
    ax2.plot(market[stock_name+"_Stock"],color='C1',label=stock_name+"_Stock")
    axes[3,0].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    # Plot five: Stock rolling correlation
    comm_pct = market["mid_price"].sort_index().pct_change()
    df = pd.DataFrame(comm_pct)
    stock_pct = market[stock_name+"_Stock"].sort_index().pct_change()
    df = df.join(stock_pct,how="outer").fillna(method="bfill")
    roll_corr = df["mid_price"].rolling(N).corr(df[stock_name+"_Stock"]).fillna(0)
    axes[3,1].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[3,1].twinx()
    ax2.bar(roll_corr.index,roll_corr,alpha=0.3,width=3,color='C2',label="Rolling_Corr")
    axes[3,1].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    # Plot four: Inventory compare
    axes[2,0].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[2,0].twinx()
    ax2.bar(market.index,market["INV"],color='C3',width=8,alpha=0.25,label="Inventory")
    y_limit = max(market["INV"])*2
    ax2.set_ylim([0,y_limit])
    axes[2,0].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    # Hist one: Distribution of RollYield
    R1 = market["r1"].dropna()
    pct_rank = R1.sort_values().values.searchsorted(R1[-1])/len(R1)
    axes[1,1].hist(R1,bins=50,color='C4',alpha=0.65)
    axes[1,1].axvline(R1[-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[1,1].get_ylim()
    axes[1,1].text(R1[-1]*1.1, top*0.9, 'Current:{:.0%},\nPct:{:.1%}'.format(R1[-1],pct_rank))
    # Hist two: Distribution of Inventory
    pct_rank = market["INV"].sort_values().values.searchsorted(market["INV"][-1])/len(market["INV"])
    axes[2,1].hist(market["INV"],bins=50,color='C3',alpha=0.65)
    axes[2,1].axvline(market["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[2,1].get_ylim()
    axes[2,1].text(market["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}'.format(market["INV"][-1],pct_rank))
    # Plot: Bond index compare
    axes[4,0].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[4,0].twinx()
    ax2.plot(market["bond_price"],color='C1',label="Bond_Cor")
    axes[4,0].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    # Plot: Bond index correlation
    comm_pct = market["mid_price"].sort_index().pct_change()
    df = pd.DataFrame(comm_pct)
    x_pct = market["bond_price"].sort_index().pct_change()
    df = df.join(x_pct,how="outer").fillna(method="bfill")
    roll_corr = df["mid_price"].rolling(N).corr(df["bond_price"]).fillna(0)
    axes[4,1].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[4,1].twinx()
    ax2.bar(roll_corr.index,roll_corr,alpha=0.3,width=3,color='C2',label="Rolling_Corr")
    axes[4,1].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    
    # Plot: USD index compare
    axes[5,0].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[5,0].twinx()
    ax2.plot(market["USD_Index"],color='C1',label="USD_Cor")
    axes[5,0].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    # Plot: USD index correlation
    comm_pct = market["mid_price"].sort_index().pct_change()
    df = pd.DataFrame(comm_pct)
    x_pct = market["USD_Index"].sort_index().pct_change()
    df = df.join(x_pct,how="outer").fillna(method="bfill")
    roll_corr = df["mid_price"].rolling(N).corr(df["USD_Index"]).fillna(0)
    axes[5,1].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[5,1].twinx()
    ax2.bar(roll_corr.index,roll_corr,alpha=0.3,width=3,color='C2',label="Rolling_Corr")
    axes[5,1].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    
    # Plot: CNYUSD index compare
    axes[6,0].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[6,0].twinx()
    ax2.plot(market["CNYUSD"],color='C1',label="CNYUSD_Cor")
    axes[6,0].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    # Plot: CNYUSD index correlation
    comm_pct = market["mid_price"].sort_index().pct_change()
    df = pd.DataFrame(comm_pct)
    x_pct = market["CNYUSD"].sort_index().pct_change()
    df = df.join(x_pct,how="outer").fillna(method="bfill")
    roll_corr = df["mid_price"].rolling(N).corr(df["CNYUSD"]).fillna(0)
    axes[6,1].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[6,1].twinx()
    ax2.bar(roll_corr.index,roll_corr,alpha=0.3,width=3,color='C2',label="Rolling_Corr")
    axes[6,1].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    
    # Plot: JPYUSD index compare
    axes[7,0].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[7,0].twinx()
    ax2.plot(market["JPYUSD"],color='C1',label="JPYUSD_Cor")
    axes[7,0].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    # Plot: JPYUSD index correlation
    comm_pct = market["mid_price"].sort_index().pct_change()
    df = pd.DataFrame(comm_pct)
    x_pct = market["JPYUSD"].sort_index().pct_change()
    df = df.join(x_pct,how="outer").fillna(method="bfill")
    roll_corr = df["mid_price"].rolling(N).corr(df["JPYUSD"]).fillna(0)
    axes[7,1].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[7,1].twinx()
    ax2.bar(roll_corr.index,roll_corr,alpha=0.3,width=3,color='C2',label="Rolling_Corr")
    axes[7,1].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    
    # Plot: WTI index compare
    axes[8,0].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[8,0].twinx()
    ax2.plot(market["WTI"],color='C1',label="WTI_Cor")
    axes[8,0].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    # Plot: WTI index correlation
    comm_pct = market["mid_price"].sort_index().pct_change()
    df = pd.DataFrame(comm_pct)
    x_pct = market["WTI"].sort_index().pct_change()
    df = df.join(x_pct,how="outer").fillna(method="bfill")
    roll_corr = df["mid_price"].rolling(N).corr(df["WTI"]).fillna(0)
    axes[8,1].plot(market["mid_price"],color='C0', label=comm_name)
    ax2 = axes[8,1].twinx()
    ax2.bar(roll_corr.index,roll_corr,alpha=0.3,width=3,color='C2',label="Rolling_Corr")
    axes[8,1].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.suptitle(comm_name.upper()+"_MarketReview", fontsize=16,y=1.01)
    plt.show()
    plt.close(fig)
    return fig