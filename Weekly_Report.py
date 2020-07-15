# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 09:02:41 2019

@author: shaolun du
@contact: shaolun.du@gmail.com
"""
import pandas as pd
import DB.fetch as fetch
import stock_currency.stock_sector as SS
import stock_currency.industry_tracking as ind_tracking
import stock_currency.get_currency as GC
from datetime import datetime, timedelta
import Market.Market_Manager as market_mgm
from Tracker_Central_Dict import weekly_dict as w_dict
""" Adjust product_name when there is more product
"""
end = datetime.today().date()- timedelta(days=0)
start = end- timedelta(days=120)

sector_weights_dict = w_dict.sector_weights_dict
col_order = w_dict.col_order

MKT = market_mgm.MKT_Manager()
""" Generate both current time market panel information
    and index price inofrmation over time
    Both files used in weekly report
"""
data_index = pd.DataFrame(fetch.get_index_all()).set_index("Dates")
data_panel = pd.DataFrame(fetch.get_panel_data(end))
sector_overview, panel, com_li = MKT.gen_market_index_v2( start, end, data_index, data_panel )
# Stock index
df_stock = SS.get_stock_sector_index(start,end,True,sector_weights_dict,col_order)
currency_df,ccy_li = GC.gen_weekly_ccy_df(start,end)
currency_df = currency_df.join(df_stock ,how ="right")[ccy_li]
currency_df = currency_df.fillna(method = "backfill")[ccy_li]

# Commodity sector
sector_overview = sector_overview.join( df_stock, how ="right",rsuffix ="_drop" )[com_li]
sector_overview = sector_overview.fillna( method = "backfill" )[com_li]

""" Start Inventory
"""
# Inventory data retriveral
inv_all = fetch.plot_inv_all("2010-01-01",end)
# Industry tracking data retriveral
in_df = ind_tracking.get_industry_data(start,end,True)
""" End Inventory
"""

""" Start Ouput to Excel
"""
writer = pd.ExcelWriter('Weekly_Data/Weekly_data.xlsx',engine='xlsxwriter')
workbook = writer.book

worksheet = workbook.add_worksheet('Currency')
writer.sheets['Currency'] = worksheet
currency_df.to_excel(writer,sheet_name='Currency',startrow=0 , startcol=0)

worksheet = workbook.add_worksheet('Stock_Sector_Overview')
writer.sheets['Stock_Sector_Overview'] = worksheet
df_stock.to_excel(writer,sheet_name='Stock_Sector_Overview',startrow=0 , startcol=0)

worksheet = workbook.add_worksheet('Commodity_Sector')
writer.sheets['Commodity_Sector'] = worksheet
sector_overview.to_excel(writer,sheet_name='Commodity_Sector',startrow=0 , startcol=0)

worksheet = workbook.add_worksheet('Panel')
writer.sheets['Panel'] = worksheet
panel.to_excel(writer,sheet_name='Panel',startrow=0 , startcol=0)

worksheet = workbook.add_worksheet('Inventory')
writer.sheets['Inventory'] = worksheet
inv_all.to_excel(writer,sheet_name='Inventory',startrow=0 , startcol=0)

worksheet = workbook.add_worksheet('Industry_Sector')
writer.sheets['Industry_Sector'] = worksheet
in_df.to_excel(writer,sheet_name='Industry_Sector',startrow=0 , startcol=0)

writer.save()

