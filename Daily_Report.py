# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 08:59:17 2019
@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
import DB.fetch as fetch
import stock_currency.stock_sector as stock
import stock_currency.industry_tracking as ind_tracking
import stock_currency.stock_tracking as stock_tracking

import pandas as pd 
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# Date format setting
pd.options.mode.chained_assignment = None  # default='warn'
secs = 1
start = dt.datetime(2016, 1, 1).date()
end = dt.date.today()-dt.timedelta(days = 1)
myFmt = mdates.DateFormatter('%y/%m')
col_names = { "Material":["Chemicals","Metals","Paper","Steel","Architecture"],
              "Discretionary":["Cars","Cloth","Media","Home_Appliance"],
              "Non-Discretionary":["Food","Wine","Beverage","Medicine","Retail"],
              "Energy":["Oil_Gas","Coal","Energy_Facility"],
              "Finance":["Bank","Insurance","Securities","Financial_Service"],
              "Medical":["Medical","Medical_Service","Biotechnology"],
              "Transportation":["Trans_Port","Trans_Road","Aviation","National_Defense"],
              "Computer":["IT_Software","IT_Hardware"],
              "Tel-Commu":["Communication_Equipment","Tel_Service","Electronic"],
              "Water-Energy":["Elec_Power","Water_Gas"],
              "Construction":["Urban_Construction","Development"],
              "Dividend":["Dividends"],
             }
code_map = [ ["IF","Shanghai"],["IH","Shanghai"],["IC","Shanghai"],
             ["T","DIVIDENS"], 
             ["AU","AU"],["AG","AU"],
             ["CU","CU"],["AL","AL"],["ZN","ZN"],
             ["PB","PB"],["SN","SN"],["NI","NI"],
             ["I","I"],["RB","REBAR"],["HC","COLS"],
             ["ZC","COAL"],["JM","COAL"],["J","COKE"],
             ["FG","FG"],
             ["SC","Shanghai"],["TA","PTA"],["PVC","PVC"],["PP","PP"],["PE","PE"],
             ["RU","RU"],["MA","MA"],["BU","BU"],["EG","Shanghai"],["SA","Shanghai"],
             ["A","Shanghai"],["M","MEAL"],["RM","MEAL"],["Y","FOOD_OIL"],["OI","FOOD_OIL"],["P","FOOD_OIL"],
             ["SR","SUGAR"],["CF","COTTON"],["C","Shanghai"],["CS","Shanghai"],["JD","Shanghai"],["AP","Shanghai"],
             ]
secotrs = {
        "Stock":["IF","IH","IC"],
        "Pre-Matels":["AU","AG"],
        "Matels":["CU","AL","ZN","PB","SN","NI"],
        "Black":["I","RB","HC","ZC","JM","J"],
        "Chem":["SC","TA","PVC","PP","PE","RU","MA","BU"],
        "Agri":["A","M","RM","Y","OI","P","SR","CF","C","CS","JD","AP"],
        }
Relative_Switch = True
# Data Preparition
index_data = pd.DataFrame(fetch.get_index_all()).set_index("Dates")
panel      = index_data.loc[end]
inv_df     = pd.DataFrame(fetch.get_historical_inventory()).set_index("Dates")
stock_data = stock.get_stock_sector_index(start,end,True,{},[],Relative_Switch)

# Plot stock industry tracking
in_df      = ind_tracking.get_industry_data(dt.datetime(2019, 1, 1).date(),end,True)

fig, axes  = plt.subplots(nrows=4, ncols=3,figsize=(12,16))
i,j = 0,0
for sector,vals in col_names.items():
    for name in vals:
        axes[i,j].plot(in_df[name],label = name)
        axes[i,j].xaxis.set_major_formatter(myFmt)
        axes[i,j].legend()
    axes[i,j].title.set_text(sector)
    j+=1
    if j == 3:
        i += 1
        j = 0
fig.autofmt_xdate()
plt.tight_layout()
plt.show()
plt.close(fig)

# Plot commodity sector products comparison
fig, axes  = plt.subplots(nrows=3, ncols=2,figsize=(12,16))
i,j = 0,0
Commpare_Plot = index_data.loc[dt.datetime(2019, 1, 1).date():]
for sector,names in secotrs.items():
    for nn in names:
        if sector == "Agri" and nn in ("CS","JD","AP"):
            # Skip some Agri product
            continue
        product = Commpare_Plot[Commpare_Plot["name"]==nn]
        product["mid"] = (product["open"]+product["close"])/2
        product["mid"] = product["mid"]/product["mid"].loc[min(product.index)]
        axes[i,j].plot(product["mid"],label=nn)
    axes[i,j].legend()
    if j == 0:
        j = 1
    else:
        j = 0
        i += 1
        
# Plot commodity-related stock industry tracking
stock_tracking.draw_product_figure(dt.datetime(2016, 1, 1).date(),end,Relative_Switch)

# Draw market panel price curves for different sector
fig, axes  = plt.subplots(nrows=3, ncols=2,figsize=(12,16))
i,j = 0,0
for sector,names in secotrs.items():
    for nn in names:
        if sector == "Agri" and nn in ("JD","AP"):
            # Skip some Agri product
            continue
        r1 = panel[panel["name"]==nn]["r1"]
        r2 = panel[panel["name"]==nn]["r2"]
        x = [0,1,2]
        y = [1,1*(1+r1),1*(1+r1)*(1+r2)]
        axes[i,j].plot(x,y,label=nn)
    axes[i,j].legend()
    if j == 0:
        j = 1
    else:
        j = 0
        i += 1

for code in code_map:
    commodity_name = code[0].upper()
    stock_name = code[1]
    # Open a blank figure
    fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(12,16))
    # Get market data
    market = index_data[index_data["name"]==commodity_name][start:]
    market["VOL/OPI"] = market["volume"]/market["opi"]
    # Get inventory data
    inventory = inv_df.loc[inv_df["Product"].str.upper()==commodity_name][start:]
    Has_Inv = True
    if len(inventory)==0:
        Has_Inv = False
    # Plot one: Market information
    axes[0,0].plot(market["close"],color='C0', label=commodity_name)
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
    axes[0,1].text(market["VOL/OPI"][-1], top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(market["VOL/OPI"][-1],pct_rank))
    
    # Plot two: Market structure (RYs)
    axes[1,0].plot(market["close"],color='C0', label=commodity_name)
    ax2 = axes[1,0].twinx()
    ax2.bar(market.index,market["r1"],alpha=0.5,width=3,color='C4', label="RollYield")
    ax2.plot(market["r1"].rolling(window = 50).std(),color='C2', alpha=0.5, label="std(RY)")
    axes[1,0].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    # Plot three: Stock compare
    axes[3,0].plot(market["close"],color='C0', label=commodity_name)
    ax2 = axes[3,0].twinx()
    ax2.plot(stock_data.index,stock_data[stock_name],color='C1',label=stock_name+"_Stock")
    axes[3,0].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    
    # Plot five: Stock rolling correlation
    N = 180
    comm_pct = market["close"].sort_index().pct_change()
    df = pd.DataFrame(comm_pct)
    stock_pct = stock_data[stock_name].sort_index().pct_change()
    df = df.join(stock_pct,how="outer").fillna(method="bfill")
    roll_corr = df["close"].rolling(N).corr(df[stock_name]).fillna(0)
    axes[3,1].plot(market["close"],color='C0', label=commodity_name)
    ax2 = axes[3,1].twinx()
    ax2.bar(roll_corr.index,roll_corr,alpha=0.3,width=3,color='C1',label="Rolling_Corr")
    axes[3,1].xaxis.set_major_formatter(myFmt)
    ax2.legend()
    # Plot four: Inventory compare
    if Has_Inv:
        axes[2,0].plot(market["close"],color='C0', label=commodity_name)
        ax2 = axes[2,0].twinx()
        ax2.bar(inventory.index,inventory["INV"],color='C3',width=8,alpha=0.25,label="Inventory")
        y_limit = max(inventory["INV"])*2
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
    if Has_Inv:
        pct_rank = inventory["INV"].sort_values().values.searchsorted(inventory["INV"][-1])/len(inventory["INV"])
        axes[2,1].hist(inventory["INV"],bins=50,color='C3',alpha=0.65)
        axes[2,1].axvline(inventory["INV"][-1], color='k', linestyle='dashed', linewidth=3)
        bottom, top = axes[2,1].get_ylim()
        axes[2,1].text(inventory["INV"][-1]*1.1, top*0.9, 'Current:{:,},\nPct:{:.1%}'.format(inventory["INV"][-1],pct_rank))
    
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.suptitle(commodity_name.upper()+"_MarketReview", fontsize=16,y=1.01)
    plt.show()
    plt.close(fig)

    