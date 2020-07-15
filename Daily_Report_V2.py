# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 22:28:07 2020

@author: shaolun du
@contact:shaolun.du@gmail.com
"""
import DB.dbFetch as dbFetch

import stock_currency.stock_handler as s_handler
import stock_currency.get_stock_sector_index as stock
import stock_currency.get_stock_industry_index as ind_tracking

import Daily_Report.draw_stock_commodity_index as D_S_plot
import Daily_Report.stock_industry_plot as S_I_plot
import Daily_Report.comm_sector_plot as C_S_plot 
import Daily_Report.comm_panel_plot as C_P_plot
import Daily_Report.single_comm_plot as S_C_plot

from Spread_Strat import Bean_Spread
from Spread_Strat import RM_Spread
from Spread_Strat import RB_Spread
from Spread_Strat import JM_Spread
from Spread_Strat import HC_Spread
from Spread_Strat import Inflation_Spread
from Spread_Strat import CA_Spread

import pandas as pd
import datetime as dt

handler = s_handler.stock_handler()

# Date format setting
pd.options.mode.chained_assignment = None  # default='warn'
end = dt.date.today()-dt.timedelta(days = 1)
Relative_Switch = True
commodity_start = dt.datetime(2019, 1, 1).date()
stock_start     = dt.datetime(2019, 1, 1).date()
spread_start    = dt.datetime(2019, 1, 1).date()

# Data Preparition
stock_data_all = handler._gen_all_ticker_df(stock_start,end)
index_data = pd.DataFrame(dbFetch.get_index_all()).set_index("Dates")
panel      = index_data.loc[end]
inv_df     = pd.DataFrame(dbFetch.get_historical_inventory()).set_index("Dates")
stock_data = stock.get_stock_sector_index_V2(stock_data_all,True,{},[],Relative_Switch)
in_df      = ind_tracking.get_industry_data_V2(stock_data_all,True)

# General Plotting
S_I_plot.plot_stock_industry( in_df )
C_S_plot.plot_commodity_sector( index_data, stock_start )
D_S_plot.plot_product_figure( stock_data_all, Relative_Switch )
C_P_plot.plot_commodity_panel( panel )
S_C_plot.plot_single_commodity( index_data, inv_df, stock_data, commodity_start )

# Spread Plotting
INF_Fig   = Inflation_Spread.gen_INF_spread(spread_start,end)
#Bean_Fig = Bean_Spread.gen_bean_spread(spread_start,end)
#RM_Fig   = RM_Spread.gen_RM_spread(spread_start,end)
#RB_Fig   = RB_Spread.gen_RB_spread(spread_start,end)
#JM_Fig   = JM_Spread.gen_JM_spread(spread_start,end)
#HC_Fig   = HC_Spread.gen_HC_spread(spread_start,end)
#CA_Fig   = CA_Spread.gen_CA_spread(spread_start,end)
