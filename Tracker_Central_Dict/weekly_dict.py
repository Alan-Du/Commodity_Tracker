# -*- coding: utf-8 -*-
"""
Created on Tue May 12 02:54:04 2020

@author: shaolun du
@contact: shaolun.du@gmail.com
"""
sector_weights_dict = {
        "Metal":[["CU","AL","ZN","PB","SN"],
                 [0.4,0.2,0.2,0.1,0.1]],
        "Black":[["I","REBAR","COLS","COKE","COAL","FG"],
                 [0.1,0.2,0.2,0.2,0.2,0.1,]],
        "Chemical":[["PTA","PVC","PP","PE","RU","BU","MA"],
                    [0.3,0.1,0.1,0.1,0.2,0.1,0.1]],
        "Agriculture":[["MEAL","SUGAR","COTTON","FOOD_OIL"],
                       [0.3,0.25,0.25,0.2]],
        }
col_order = [ "Shanghai",
              "AU","CU","AL","ZN","PB","SN","NI",
              "I","REBAR","COLS","COKE","COAL","FG",
              "PTA","PVC","PP","PE","RU","BU","MA",
              "MEAL","SUGAR","COTTON","FOOD_OIL",
              "DIVIDENS",
              "Metal","Black","Chemical","Agriculture",
            ]

