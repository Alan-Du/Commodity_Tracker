# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 03:56:02 2020

@author: shaolun du
@contact: Shaolun.du@gmail.com
"""
def gen_two_product_spread( Ticker_1,Ticker_2,
                            start,end ):
    import DB.fetch as fetch
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    #This is a helper function for two product spread calculation
    myFmt = mdates.DateFormatter('%y/%m') # Dates format
    #Get raw market data
    index_data = pd.DataFrame(fetch.get_index_all()).set_index("Dates")
    inv_df = pd.DataFrame(fetch.get_historical_inventory()).set_index("Dates")
    
    market_1 = index_data[index_data["name"]==Ticker_1][start:end]
    market_1["mid_price"] = 0.5*(market_1["open"]+market_1["close"])
    market_1["mid_price"] = market_1["mid_price"]/market_1["mid_price"][0]
    market_1 = market_1[["mid_price","r1"]]
    Inventory = inv_df.loc[inv_df["Product"].str.upper()==Ticker_1][start:end]["INV"]
    market_1 = market_1.join( Inventory, how="left" ).fillna(method='ffill')
    
    
    market_2 = index_data[index_data["name"]==Ticker_2][start:end]
    market_2["mid_price"] = 0.5*(market_2["open"]+market_2["close"])
    market_2["mid_price"] = market_2["mid_price"]/market_2["mid_price"][0]
    market_2 = market_2[["mid_price","r1"]]
    Inventory = inv_df.loc[inv_df["Product"].str.upper()==Ticker_2][start:end]["INV"]
    market_2 = market_2.join(Inventory,how="left").fillna(method='ffill')
    
    # Start plotting
    #Fig1: Bean and Bean Meal spread plot
    #Subplot 1,2: spread and spread distribution
    spread_name = Ticker_1+"_"+Ticker_2+"_Spread"
    fig, axes = plt.subplots(nrows=5, ncols=2,figsize=(10,20))    
    market_1[spread_name] = market_1["mid_price"]-market_2["mid_price"]
    axes[0,0].plot(market_1[spread_name],color='C0', label=Ticker_1+"-"+Ticker_2)
    axes[0,0].legend()
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
    R1 = market_1["r1"].dropna()
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
    R1 = market_2["r1"].dropna()
    pct_rank = R1.sort_values().values.searchsorted(R1[-1])/len(R1)
    axes[2,1].hist(R1,bins=50,color='C4',alpha=0.65)
    axes[2,1].axvline(R1[-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[2,1].get_ylim()
    axes[2,1].text(R1[-1]*1.1, top*0.9, 'Current:{:.0%},\nPct:{:.1%}'.format(R1[-1],pct_rank))
    
    axes[3,0].bar(market_1.index,market_1["INV"],alpha=0.5,width=3,color='C4', label=Ticker_1+"_INV")
    axes[3,0].legend()
    pct_rank = market_1["INV"].sort_values().values.searchsorted(market_1["INV"][-1])/len(market_1["INV"])
    axes[3,1].hist(market_1["INV"],bins=50,color='C3',alpha=0.65)
    axes[3,1].axvline(market_1["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[3,1].get_ylim()
    axes[3,1].text(market_1["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}\nDate:{:%d.%m.%Y}'.format(market_1["INV"][-1],pct_rank,market_1.index[-1]))
    
    axes[4,0].bar(market_2.index,market_2["INV"],alpha=0.5,width=3,color='C4', label=Ticker_2+"_INV")
    axes[4,0].legend()
    pct_rank = market_2["INV"].sort_values().values.searchsorted(market_2["INV"][-1])/len(market_2["INV"])
    axes[4,1].hist(market_2["INV"],bins=50,color='C3',alpha=0.65)
    axes[4,1].axvline(market_2["INV"][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[4,1].get_ylim()
    axes[4,1].text(market_2["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}\nDate:{:%d.%m.%Y}'.format(market_2["INV"][-1],pct_rank,market_2.index[-1]))
    
    fig.suptitle(Ticker_1+"/"+Ticker_2+" Spread Strat",y=0.9)
    return fig

def gen_two_product_spread_SIMPLE( Ticker_1,Ticker_2, start,end ):
    import DB.fetch as fetch
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    #This is a helper function for two product spread calculation
    myFmt = mdates.DateFormatter('%y/%m') # Dates format
    #Get raw market data
    index_data = pd.DataFrame(fetch.get_index_all()).set_index("Dates")

    market_1 = index_data[index_data["name"]==Ticker_1][start:end]
    market_1["mid_price"] = 0.5*(market_1["open"]+market_1["close"])
    market_1["mid_price"] = market_1["mid_price"]/market_1["mid_price"][0]
    market_1 = market_1[["mid_price","r1"]]
    
    market_2 = index_data[index_data["name"]==Ticker_2][start:end]
    market_2["mid_price"] = 0.5*(market_2["open"]+market_2["close"])
    market_2["mid_price"] = market_2["mid_price"]/market_2["mid_price"][0]
    market_2 = market_2[["mid_price","r1"]]
    
    # Start plotting
    #Fig1: Bean and Bean Meal spread plot
    #Subplot 1,2: spread and spread distribution
    spread_name = Ticker_1+"_"+Ticker_2+"_Spread"
    fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(12,5))    
    market_1[spread_name] = market_1["mid_price"]-market_2["mid_price"]
    axes[0].plot(market_1[spread_name],color='C0', label=Ticker_1+"-"+Ticker_2)
    axes[0].legend()
    axes[1].hist(market_1[spread_name],bins=50,color='C1', label=spread_name)
    axes[1].axvline(market_1[spread_name][-1], color='k', linestyle='dashed', linewidth=3)
    bottom, top = axes[1].get_ylim()
    pct_rank = market_1[spread_name].sort_values().values.searchsorted(market_1[spread_name][-1])/len(market_1[spread_name])
    axes[1].text(market_1[spread_name][-1], top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(market_1[spread_name][-1],pct_rank))
    axes[0].xaxis.set_major_formatter(myFmt)
    
    fig.suptitle(Ticker_1+"/"+Ticker_2+" Spread Strat")
    return fig