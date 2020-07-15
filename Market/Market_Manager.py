# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 12:06:21 2019

@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
import os
import pandas as pd
from sector_weights import set_sector_weights as set_sector_weights
from cal_weighted_average import wavg
class MKT_Manager:
    """ Market manager: collect market data
        generate market index and key market 
        price signals
    """
    def __init__(self):
        self.cur_path = os.path.dirname(os.path.abspath(__file__))
        self.parent_path = os.path.dirname(self.cur_path)
    
    def gen_market_index_v2( self, start, end,
                             data_index, data_panel ):
        # Generate market index table directly
        # from commodity market index database
        # Return current time market panel information 
        panel = data_panel[["Dates","Code","Open","High","Low","Close","OPI","Vol"]]
        data_index = data_index[(data_index.index>=start) & (data_index.index<=end)]
        # Return market index price overtime
        sector_weight = set_sector_weights()
        sector_overview = pd.DataFrame()
        for block in sector_weight:
            ans = pd.DataFrame()
            sector = block[0]
            for ss in sector:
                temp = data_index.loc[data_index["name"]==ss]
                temp = temp[["close"]].rename(columns={"close":ss})
                temp[ss] = temp[ss]/temp[ss].iloc[0]
                ans = ans.join( temp, how = "outer").fillna(method='backfill')
            sector_overview = sector_overview.join( ans, how = "outer")
            i = 0
            for nn in block[0]:
                ans[nn] = ans[nn]*block[2][i]
                i = i+1
            sector_overview[block[1]] = ans.sum(axis = 1)
        sector_overview = sector_overview.fillna(method="backfill")
        # Reorder columns
        cols = sector_overview.columns.tolist()
        index_cols = ["Metal","Black_Cons","Chemistry","Agriculture","Stock","Bond"]
        prod_cols  = [x for x in cols if x not in index_cols]
        sector_overview = sector_overview[index_cols+prod_cols]
        return sector_overview, panel, index_cols+prod_cols
    
    def gen_market_index_raw(self,df = []):
        # Generate raw price index for all datapint
         # Return current time market panel information 
        # Return market index price overtime
        sector_weight = set_sector_weights()
        sector_overview = pd.DataFrame()
        for blcok in sector_weight:
            ans = pd.DataFrame()
            sector = blcok[0]
            for ss in sector:
                i_str = ss+"\d+"
                temp = df.loc[(df["Code"].str.match(i_str))&(df["Code"].str.len()<10)]
                temp = temp.groupby("Dates").apply(wavg, "Close", "OPI")
                temp = temp.rename(ss)
                ans = ans.join( temp, how = "outer").fillna(method='backfill')
            sector_overview = sector_overview.join( ans, how = "outer")
            i = 0
            for nn in blcok[0]:
                ans[nn] = ans[nn]*blcok[2][i]
                i = i+1
            sector_overview[blcok[1]] = ans.sum(axis = 1)
        sector_overview = sector_overview.fillna(method="backfill")
        # Reorder columns
        cols = sector_overview.columns.tolist()
        index_cols = ["Metal","Black_Cons","Chemistry","Agriculture","Stock","Bond"]
        prod_cols  = [x for x in cols if x not in index_cols]
        sector_overview = sector_overview[index_cols+prod_cols]
        return sector_overview, index_cols+prod_cols
