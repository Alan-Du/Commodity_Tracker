# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 00:40:10 2020

@author: shaolun du
@contact: Shaolun.du@gmail.com
"""
import datetime as dt
from Spread_Strat import Bean_Spread
from Spread_Strat import RM_Spread
from Spread_Strat import RB_Spread
from Spread_Strat import JM_Spread
from Spread_Strat import HC_Spread
from Spread_Strat import Inflation_Spread
from Spread_Strat import Spread_Helper
from Spread_Strat import CA_Spread

start = dt.datetime(2014, 1, 1).date()
end = dt.date.today()-dt.timedelta(days = 1)

#INF_Fig   = Inflation_Spread.gen_INF_spread(start,end)
#
Bean_Fig = Bean_Spread.gen_bean_spread(start,end)
#RM_Fig   = RM_Spread.gen_RM_spread(start,end)
#RB_Fig   = RB_Spread.gen_RB_spread(start,end)
#JM_Fig   = JM_Spread.gen_JM_spread(start,end)
#HC_Fig   = HC_Spread.gen_HC_spread(start,end)
#
#CA_Fig   = CA_Spread.gen_CA_spread(start,end)
#spread_all = [["I","RB"],["RB","HC"],["J","JM"],["I","J"],["A","M"],
#              ["M","RM"],["M","Y"],["RM","OI"],["Y","OI"],["Y","P"],
#              ["A","C"],["C","CS"],["C","M"],["TA","BU"],["PVC","PP"],
#              ["TA","PE"],["MA","PP"]]
#X_Fig = Spread_Helper.gen_two_product_spread_SIMPLE("CU","RU",start,end)
#X_Fig = Spread_Helper.gen_two_product_spread_SIMPLE("IC","ZC",start,end)
#X_Fig = Spread_Helper.gen_two_product_spread_SIMPLE("IC","JM",start,end)