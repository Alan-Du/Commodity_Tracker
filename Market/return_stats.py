# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 08:59:17 2019

@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
import pandas as pd
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
        df = pd.DataFrame(val,columns = ["Dates","Return%","Quantile"])
        df["Product"] = key
        df = df[["Dates","Product","Return%","Quantile"]]
        ans_df = ans_df.append(df)
    ans_df = ans_df.set_index("Dates").sort_index()
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
        df = pd.DataFrame(val,columns = ["Dates","Skewness","%Positive"])
        df["Product"] = key
        df = df[["Dates","Product","Skewness","%Positive"]]
        ans_df = ans_df.append(df)
    ans_df = ans_df.set_index("Dates").sort_index()
    return ans_df 
