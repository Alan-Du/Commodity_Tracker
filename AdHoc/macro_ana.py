# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 13:42:22 2019

@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import datetime as dt
import numpy as np
# Paramater Setting
start = dt.datetime(2010,1,1)
end   = dt.datetime(2019,12,31)
window = 100


f_name = "China_Macro.xlsx"
df = pd.read_excel(f_name).set_index("Dates")
mask = (df.index > start) & (df.index <= end)
df = df[mask].sort_index()

# Step One calculate percentage deviation
roll = df.rolling(window=window).mean()
std_df = ((df-roll)/roll)

std_df["Stock_Bond"] = (std_df["Stock"].rolling(window).corr(std_df["Bond"]))
std_df["Stock_RMB"] = (std_df["Stock"].rolling(window).corr(std_df["RMB"]))
std_df["Stock_JPY"] = (std_df["Stock"].rolling(window).corr(std_df["JPY"]))
std_df["Stock_Gold"] = (std_df["Stock"].rolling(window).corr(std_df["Gold"]))
std_df["Stock_Oil"] = (std_df["Stock"].rolling(window).corr(std_df["Gold"]))
std_df = std_df.dropna()
df = df[df.index.isin(std_df.index)] # Reshape original dataframe


x_name = "Stock"
y_name = "RMB"
band_width_1 = 0.005
band_width_2 = 0.01
f = plt.figure(figsize=(8,20))
ax1=f.add_subplot(313)
std_df.plot.scatter(ax = ax1,x=x_name,y=y_name)
plt.axhline(band_width_1, color='red')
plt.axhline(-band_width_1, color='red')
plt.axvline(band_width_2, color='red')
plt.axvline(-band_width_2, color='red')
plt.title("(Price-MA)/MA Scatter")


band_width_3 = 0.6
ax2=f.add_subplot(312)
std_df[x_name+"_"+y_name].plot(ax = ax2)
plt.axhline(band_width_3, color='red')
plt.axhline(-band_width_3, color='red')
plt.title("Rolling Correlation Plot")

ax3=f.add_subplot(311)
mask_pos = np.ma.masked_where(std_df[x_name+"_"+y_name] <= band_width_3, df["Stock"])
mask_neg = np.ma.masked_where(std_df[x_name+"_"+y_name] >= -band_width_3, df["Stock"])
middle   = np.ma.masked_where((std_df[x_name+"_"+y_name] <= -band_width_3) | (std_df[x_name+"_"+y_name] >= band_width_3), df["Stock"])
ax3.plot( std_df.index, mask_pos,'r',
          std_df.index, mask_neg,'g',
          std_df.index, middle,'b' )
plt.title("Stock Price")
plt.tight_layout()
plt.savefig('Compare.png')