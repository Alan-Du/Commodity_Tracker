# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 08:59:17 2019

@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
import pandas as pd
import datetime
def relative_strong_signal(data,threshold,val_threshold):
    """ This function compute date based sectional 
        relative strong/weak indicator given dataframe with
        structure = {"row":"dates","col":"product price"}
        we select the dates when market overal drops/raise
        but a very small portion(threshold) of it goes opposite
        Output dataframe gives relative strong/weak indicator
        with that date return and associated quantile
    """
    answers = {} # Output={"Product":[Dates,return,threshold]..}
    ans_df = pd.DataFrame() # Reordering answer dataframe [df1,df2]
    # Provide data in pandas dataframe
    df = data.pct_change().dropna().round(5)
    total = df.shape[1]
    for index, row in df.iterrows():
        positive_pct = round(sum(row>0)/total,3)
        negative_pct = round(sum(row<0)/total,3)
        if positive_pct <= threshold:
            temp = row.where(row>0).dropna().to_dict()
            for key,val in temp.items():
                val = val*100
                if abs(val) > val_threshold:
                    if key not in answers:
                        answers[key] = [[index.date(),val,positive_pct]]
                    else:
                        answers[key].append([index.date(),val,positive_pct])
        elif negative_pct <= threshold:
            temp = row.where(row<0).dropna().to_dict()
            for key,val in temp.items():
                val = val*100
                if abs(val) > val_threshold:
                    if key not in answers:
                        answers[key] = [[index.date(),val,negative_pct]]
                    else:
                        answers[key].append([index.date(),val,negative_pct])
    for key,val in answers.items():
        df = pd.DataFrame(val,columns = ["Date","Return%","Quantile"])
        df["Product"] = key
        df = df[["Date","Product","Return%","Quantile"]]
        ans_df = ans_df.append(df)
    ans_df = ans_df.set_index("Date").sort_index()
    return ans_df

def relative_skew_signal( data, window,
                          Top_NUM, val_tao ):
    """ This function compute date based sectional 
        relative skewness indicator given dataframe with
        structure = {"row":"dates","col":"product price"}
        we select the dates when market overal skewness is one side
        but a very small portion(threshold) of it goes opposite
        Output dataframe gives relative strong/weak indicator
        with that date return and associated quantile
    """
    answers = {} # Output={"Product":[Dates,return,threshold]..}
    ans_df = pd.DataFrame() # Reordering answer dataframe [df1,df2]
    # Provide data in pandas dataframe
    df = data.pct_change().dropna().round(5)
    total = df.shape[1]
    for i in range(window,df.shape[0]):
        sDate = df.index[i]
        skewness = df[i-window:i].skew()
        positive_pct = round(sum(skewness>0)/total,3)
        temp = skewness.nlargest(Top_NUM).to_dict()
        for key,val in temp.items():
            if abs(val)>val_tao:
                if key not in answers:
                    answers[key] = [[sDate.date(),val,positive_pct]]
                else:
                    answers[key].append([sDate.date(),val,positive_pct])
        temp = skewness.nsmallest(Top_NUM).to_dict()
        for key,val in temp.items():
            if abs(val)>val_tao:
                if key not in answers:
                    answers[key] = [[sDate.date(),val,positive_pct]]
                else:
                    answers[key].append([sDate.date(),val,positive_pct])
    for key,val in answers.items():
        df = pd.DataFrame(val,columns = ["Date","Skewness","%Positive"])
        df["Product"] = key
        df = df[["Date","Product","Skewness","%Positive"]]
        ans_df = ans_df.append(df)
    ans_df = ans_df.set_index("Date").sort_index()
    return ans_df

def MDI_window(df,windows):
    # Calculate all MDI given windows
    ans = pd.DataFrame()
    for wind in windows:
        mask = (df.index > wind[0]) & (df.index <= wind[1])
        data = df.loc[mask]
        MDI = (data.iloc[-1]-data.iloc[0])/data.diff().abs().sum()
        MDI["Dates"] = wind[0]
        ans = ans.append(MDI,ignore_index=True)
    ans = ans.set_index("Dates")
    return ans

#df = pd.read_excel("Commodity_Sector.xlsx").set_index("Dates")
#windows = [ ["2018-04-19","2018-11-07"],
#            ["2019-04-03","2019-06-03"],
#            ["2019-07-13","2019-09-03"] ]
#MDI = MDI_window(df,windows)
#MDI.to_excel("MDI.xlsx")
#print(MDI)
