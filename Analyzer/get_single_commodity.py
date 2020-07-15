# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 05:29:54 2020
Get single commodity price historical data frame
@author: shaolun du
@contact: shaolun.du@gmail.com
"""
import pandas as pd
import DB.dbFetch as dbFetch
def get_single_commodity( start, end,
                          ticker, 
                          has_INV = False):
    index_data = pd.DataFrame(dbFetch.get_index_all()).set_index("Dates")
    market = index_data[index_data["name"]==ticker][start:end]
    market["VOL/OPI"] = market["volume"]/market["opi"]
    market["mid_price"] = 0.5*(market["open"]+market["close"])
    market = market[["mid_price","opi","volume","r1","r2","VOL/OPI"]]
    if has_INV:
        inv_df = pd.DataFrame(dbFetch.get_historical_inventory()).set_index("Dates")
        inventory = inv_df.loc[inv_df["Product"].str.upper()==ticker][start:end]["INV"]
        market = market.join(inventory,how="left")
    return market
