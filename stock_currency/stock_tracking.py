#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 14:16:36 2019

@author: shaolundu
@contact: Shaolun.du@gmail.com
"""
from stock_currency import product_dict as P_d
from stock_currency import stock_helper as helper
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib.dates import DateFormatter

def draw_product_figure(start,end, relative=False):
    myFmt = DateFormatter("%y-%m") # Date formatter
    
    fig0, axes = plt.subplots(nrows=2, ncols=3,figsize=(12,8))
    df = helper.get_industry_index(start,end,P_d.COPPER,relative)
    for name in P_d.COPPER.keys():
        if name != "ShangHai_Index":
            axes[0,0].plot(df[name],label = name)
            axes[0,0].xaxis.set_major_formatter(myFmt)
    axes[0,0].title.set_text('COPPER Sector')
    axes[0,0].legend()
    
    df = helper.get_industry_index(start,end,P_d.ALUMINUM,relative)
    for name in P_d.ALUMINUM.keys():
        if name != "ShangHai_Index":
            axes[0,1].plot(df[name],label = name)
            axes[0,1].xaxis.set_major_formatter(myFmt)
    axes[0,1].title.set_text('ALUMINUM Sector')
    axes[0,1].legend()
    
    
    df = helper.get_industry_index(start,end,P_d.ZINC,relative)
    for name in P_d.ZINC.keys():
        if name != "ShangHai_Index":
            axes[0,2].plot(df[name],label = name)
            axes[0,2].xaxis.set_major_formatter(myFmt)
    axes[0,2].title.set_text('ZINC Sector')
    axes[0,2].legend()
    
    df = helper.get_industry_index(start,end,P_d.PB,relative)
    for name in P_d.PB.keys():
        if name != "ShangHai_Index":
            axes[1,0].plot(df[name],label = name)
            axes[1,0].xaxis.set_major_formatter(myFmt)
    axes[1,0].title.set_text('PB Sector')
    axes[1,0].legend()
    
    df = helper.get_industry_index(start,end,P_d.NI,relative)
    for name in P_d.NI.keys():
        if name != "ShangHai_Index":
            axes[1,1].plot(df[name],label = name)
            axes[1,1].xaxis.set_major_formatter(myFmt)
    axes[1,1].title.set_text('NI Sector')
    axes[1,1].legend()
    
    df = helper.get_industry_index(start,end,P_d.SN,relative)
    for name in P_d.SN.keys():
        if name != "ShangHai_Index":
            axes[1,2].plot(df[name],label = name)
            axes[1,2].xaxis.set_major_formatter(myFmt)
    axes[1,2].title.set_text('SN Sector')
    axes[1,2].legend()
    fig0.tight_layout()
    
    fig1, axes = plt.subplots(nrows=2, ncols=2,figsize=(8,8))
    
    df = helper.get_industry_index(start,end,P_d.ORE,relative)
    for name in P_d.ORE.keys():
        if name != "ShangHai_Index":
            axes[0,0].plot(df[name],label = name)
            axes[0,0].xaxis.set_major_formatter(myFmt)
    axes[0,0].title.set_text('ORE Sector')
    axes[0,0].legend()
    
    df = helper.get_industry_index(start,end,P_d.STEEL,relative)
    for name in P_d.STEEL.keys():
        if name != "ShangHai_Index":
            axes[0,1].plot(df[name],label = name)
            axes[0,1].xaxis.set_major_formatter(myFmt)
    axes[0,1].title.set_text('STEEL Sector')
    axes[0,1].legend()
    
    df = helper.get_industry_index(start,end,P_d.COAL,relative)
    for name in P_d.COAL.keys():
        if name != "ShangHai_Index":
            axes[1,0].plot(df[name],label = name)
            axes[1,0].xaxis.set_major_formatter(myFmt)
    axes[1,0].title.set_text('COAL Sector')
    axes[1,0].legend()
    
    df = helper.get_industry_index(start,end,P_d.GLASS,relative)
    for name in P_d.GLASS.keys():
        if name != "ShangHai_Index":
            axes[1,1].plot(df[name],label = name)
            axes[1,1].xaxis.set_major_formatter(myFmt)
    axes[1,1].title.set_text('GLASS Sector')
    axes[1,1].legend()
    
    fig1.tight_layout()
    
    
    fig2, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,12))
    
    df = helper.get_industry_index(start,end,P_d.PTA,relative)
    for name in P_d.PTA.keys():
        if name != "ShangHai_Index":
            axes[0,0].plot(df[name],label = name)
            axes[0,0].xaxis.set_major_formatter(myFmt)
    axes[0,0].title.set_text('PTA Sector')
    axes[0,0].legend()
    
    df = helper.get_industry_index(start,end,P_d.PP,relative)
    for name in P_d.PP.keys():
        if name != "ShangHai_Index":
            axes[0,1].plot(df[name],label = name)
            axes[0,1].xaxis.set_major_formatter(myFmt)
    axes[0,1].title.set_text('PP Sector')
    axes[0,1].legend()
    
    df = helper.get_industry_index(start,end,P_d.PVC,relative)
    for name in P_d.PVC.keys():
        if name != "ShangHai_Index":
            axes[1,0].plot(df[name],label = name)
            axes[1,0].xaxis.set_major_formatter(myFmt)
    axes[1,0].title.set_text('PVC Sector')
    axes[1,0].legend()
    
    df = helper.get_industry_index(start,end,P_d.BU,relative)
    for name in P_d.BU.keys():
        if name != "ShangHai_Index":
            axes[1,1].plot(df[name],label = name)
            axes[1,1].xaxis.set_major_formatter(myFmt)
    axes[1,1].title.set_text('BU Sector')
    axes[1,1].legend()
    
    df = helper.get_industry_index(start,end,P_d.RUBBER,relative)
    for name in P_d.RUBBER.keys():
        if name != "ShangHai_Index":
            axes[2,0].plot(df[name],label = name)
            axes[2,0].xaxis.set_major_formatter(myFmt)
    axes[2,0].title.set_text('RUBBER Sector')
    axes[2,0].legend()
    
    df = helper.get_industry_index(start,end,P_d.PE,relative)
    for name in P_d.PE.keys():
        if name != "ShangHai_Index":
            axes[2,1].plot(df[name],label = name)
            axes[2,1].xaxis.set_major_formatter(myFmt)
    axes[2,1].title.set_text('PE Sector')
    axes[2,1].legend()
    
    df = helper.get_industry_index(start,end,P_d.MA,relative)
    for name in P_d.MA.keys():
        if name != "ShangHai_Index":
            axes[3,0].plot(df[name],label = name)
            axes[3,0].xaxis.set_major_formatter(myFmt)
    axes[3,0].title.set_text('MA Sector')
    axes[3,0].legend()
    
    fig2.tight_layout()
    
    
    fig3, axes = plt.subplots(nrows=2, ncols=2,figsize=(8,8))
    
    df = helper.get_industry_index(start,end,P_d.SUGAR,relative)
    for name in P_d.SUGAR.keys():
        if name != "ShangHai_Index":
            axes[0,0].plot(df[name],label = name)
            axes[0,0].xaxis.set_major_formatter(myFmt)
    axes[0,0].title.set_text('SUGAR Sector')
    axes[0,0].legend()
    
    df = helper.get_industry_index(start,end,P_d.FOOD_OIL,relative)
    for name in P_d.FOOD_OIL.keys():
        if name != "ShangHai_Index":
            axes[0,1].plot(df[name],label = name)
            axes[0,1].xaxis.set_major_formatter(myFmt)
    axes[0,1].title.set_text('FOOD_OIL Sector')
    axes[0,1].legend()
    
    df = helper.get_industry_index(start,end,P_d.MEAL,relative)
    for name in P_d.MEAL.keys():
        if name != "ShangHai_Index":
            axes[1,0].plot(df[name],label = name)
            axes[1,0].xaxis.set_major_formatter(myFmt)
    axes[1,0].title.set_text('MEAL Sector')
    axes[1,0].legend()
    
    df = helper.get_industry_index(start,end,P_d.COTTON,relative)
    for name in P_d.COTTON.keys():
        if name != "ShangHai_Index":
            axes[1,1].plot(df[name],label = name)
            axes[1,1].xaxis.set_major_formatter(myFmt)
    axes[1,1].title.set_text('COTTON Sector')
    axes[1,1].legend()
    
    fig3.tight_layout()
    
    return fig0,fig2,fig1,fig3


#end = dt.datetime.today().date()
#start = dt.datetime(2019,1,1).date()
#relative_twitch = True
#fig0,fig1,fig2,fig3 = draw_product_figure(start,end,relative_twitch)


