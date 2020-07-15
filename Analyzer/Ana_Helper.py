# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 08:59:17 2019
This is tools function for Analyzer
@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
import pandas as pd
import numpy as np
    
def get_single_name_index(data, name):
    def cal_roll_yield(x):
        # Helper function after groupby
        if len(x) == 3:
            diffd1 = (x.iloc[1]["Maturity"]-x.iloc[0]["Maturity"]).days/365
            diff1 = (x.iloc[1]["Close"]-x.iloc[0]["Close"])/x.iloc[0]["Close"]
            R1 = diff1/diffd1
            diffd2 = (x.iloc[2]["Maturity"]-x.iloc[1]["Maturity"]).days/365
            diff2 = (x.iloc[2]["Close"]-x.iloc[1]["Close"])/x.iloc[1]["Close"]
            R2 = diff2/diffd2
        elif len(x) == 2:
            diffd1 = (x.iloc[1]["Maturity"]-x.iloc[0]["Maturity"]).days/365
            diff1 = (x.iloc[1]["Close"]-x.iloc[0]["Close"])/x.iloc[0]["Close"]
            R1 = diff1/diffd1
            R2 = 0
        else:
            R1 = 0
            R2 = 0
        return pd.Series({'R1':R1,'R2':R2})
    data["Code"] = data["Code"].str.strip()
    single = data.loc[data["Code"].str.match(name+"\d+")]
    single = single.sort_values(by=["Dates","OPI"],ascending=False).groupby("Dates").head(3)
    single["Y"] = pd.to_datetime(single["Dates"]).dt.year.astype(str)
    code_len = len(single["Code"].iloc[0].replace(name,""))
    if code_len == 4:
        single["Maturity"] = single["Y"].str[:2]+single["Code"].str.replace(name,"")+"01"
    elif code_len == 3:
        single["Maturity"] = single["Y"].str[:3]+single["Code"].str.replace(name,"")+"01"
    single["Maturity"] = pd.to_datetime(single["Maturity"])
    rolls = single.sort_values(by=["Dates","Maturity"]).groupby("Dates").apply(cal_roll_yield)
    rolls["Price"] = single.groupby("Dates").mean()["Close"]
    rolls["Vol"] = single.groupby("Dates").mean()["Vol"]
    rolls["OPI"] = single.groupby("Dates").mean()["OPI"]
    rolls["Name"] = name.upper()
    return rolls

def get_cor_skew_df( data, stock_data=[], name_li = [] ):
    # Need stock data as inputs gets from stock analyzer
    from collections import OrderedDict
    name_li = [ ['AG','AU'],['AU','AU'],
            ['CU','CU'], ['AL','AL'], ['ZN','ZN'],['PB','PB'],['NI','NI'],['SN','SN'],
            ['ZC','COAL'],['JM','COAL'],['J','COKE'],
            ['I','I'],['RB','REBAR'],['HC','COLS'],['FG','FG'],
            ['TA','PTA'], ['PVC','PVC'], ['PP','PP'], ['PE','PE'], 
            ['RU','RU'],['BU','BU'],['MA','MA'], 
            ['A','Shanghai'],['M','MEAL'],['RM','MEAL'],
            ['Y','FOOD_OIL'],['OI','FOOD_OIL'],['P','FOOD_OIL'],
            ['SR','SUGAR'],['CF','COTTON'],['JD','Shanghai'],['CS','Shanghai'],['C','Shanghai'],
            ['IC','Shanghai'],['IF','Shanghai'], ['IH','Shanghai'],
            ['T','DIVIDENS'], ['TF','DIVIDENS'],['TS','DIVIDENS'],
            ]
    N = 52
    stock_df = stock_data.sort_index().asfreq(freq='W-Fri', how='start', method='ffill').pct_change()
    answer = OrderedDict()
    col_names = ["Skew","Ret","Q10","Q90","Corr_Stock"]
    for n1 in range(len(name_li)):
        temp_dict = OrderedDict()
        df1 = data[data["name"]==name_li[n1][0]]
        df1 = df1.asfreq(freq='W-Fri', how='start', method='ffill')
        df1["Ret"] = df1["close"].pct_change()
        Q_1 = df1["Ret"].quantile(0.1)
        Q_2 = df1["Ret"].quantile(0.9)
        skew_1 = df1.iloc[-N:]["Ret"].skew()
        temp_dict["Ret"] = df1.iloc[-1]["Ret"]
        temp_dict["Skew"] = skew_1
        temp_dict["Q10"] = Q_1
        temp_dict["Q90"] = Q_2
        Corr_stock = df1["Ret"].corr(stock_df[name_li[n1][1]])
        temp_dict["Corr_Stock"] = Corr_stock
        for n2 in range(len(name_li)):
            df2 = data[data["name"]==name_li[n2][0]]
            df2 = df2.asfreq(freq='W-Fri', how='end', method='ffill')
            df2["Ret"] = df2["close"].pct_change()
            Corr_X = df1["Ret"].corr(df2["Ret"])
            temp_dict["Cor_"+name_li[n2][0]] = Corr_X
            if "Cor_"+name_li[n2][0] not in col_names:
                col_names.append("Cor_"+name_li[n2][0])
        answer[name_li[n1][0]] = temp_dict
    df = pd.DataFrame(answer).T.round(2)[col_names]
    return df

def count_pos_prob(df, col_name, freq_M, start):
    # Input: df with date indexed,
    #        target columns name
    # Output: count of positive return probabilit
    pivot_tb = pd.DataFrame()
    for col in col_name:
        df_col = df.loc[df["name"]==col][["close"]]
        df_col = df_col.rename(columns = {"close":col})
        if pivot_tb.empty:
            pivot_tb = df_col
        else:
            pivot_tb = pivot_tb.join(df_col)
    pivot_tb = pivot_tb.loc[pivot_tb.index>=start].interpolate(method ='linear', limit_direction ='forward') 
    day_rng = pd.date_range(pivot_tb.index[0], pivot_tb.index[-1], freq='D', closed='left')
    pivot_tb = pivot_tb.reindex(day_rng, method='ffill')
    df_freq = pivot_tb.asfreq(freq="M").pct_change()
    df_freq['Month'] = df_freq.index.month
    re_name = ["P_"+col for col in col_name]
    df_freq[re_name] = df_freq[col_name].pct_change()
    grouped = df_freq.groupby(['Month'])[re_name].apply(lambda x:(x>0).sum()/x.count())
    grouped = grouped.round(2)
    return grouped.T

def get_ZZ_maturity(row,code):
    # Generate maturity code for 
    # ZZ exchange NOTE: they have a wired 
    # format which only use 3 digits to 
    # represent matruity 
    code_year = int(row["Code"][len(code):len(code)+1]) # Take code yesr last digit
    curr_year = int(str(row["Dates"].year)[-1]) # Take current year last digit
    if curr_year != code_year:
        code_year = str(row["Dates"].year+1)
    else:
        code_year = str(row["Dates"].year)
    maturity = code_year+row["Code"][-2:]+"01"
    return maturity

def get_maturity(row,code):
    maturity = str(row["Dates"].year)[:2]+row["Code"][len(code):]+"01"
    return maturity

def gen_maturity( code,
                  data ):
    # Generate matruity date given
    # code and current date
    # Matruity will all assume at first day of month
    exchange_map = { "a":"DL","b":"DL","eg":"DL","jm":"DL","j":"DL",
                     "i":"DL","pvc":"DL","pp":"DL","pe":"DL","m":"DL",
                     "y":"DL","p":"DL","jd":"DL","cs":"DL","c":"DL",
                     "au":"SH","ag":"SH","cu":"SH","al":"SH","zn":"SH",
                     "pb":"SH","sn":"SH","ni":"SH","rb":"SH","hc":"SH",
                     "sc":"SH","bu":"SH","ru":"SH",
                     "AP":"ZZ","CF":"ZZ","FG":"ZZ","MA":"ZZ","OI":"ZZ",
                     "RM":"ZZ","SR":"ZZ","TA":"ZZ","ZC":"ZZ",
                     "IC":"ZJ","IH":"ZJ","IF":"ZJ","T":"ZJ","TS":"ZJ",
                     "TF":"ZJ",
                    }
    exchange_name = exchange_map[code]
    data["Code"] = data["Code"].str.strip() # Make sure no space in code
    if exchange_name == "ZZ":
        data["Maturity"] = pd.to_datetime(data.apply(get_ZZ_maturity,axis=1,args=[code]))
    else:
        data["Maturity"] = pd.to_datetime(data.apply(get_maturity,axis=1,args=[code]))
    return data
    
def get_single_name_price( code, data=[] ):
    N = 55 # Rolling window
    ans = [] #Return value
    data = data.loc[data["Code"].str.match(code+"\d+")]
    # Get maturity code, within 100year first two digit will not change
    data = gen_maturity( code, data )
    grouped = data.groupby("Dates")
    NUM_AVG = 2
    for name, group in grouped:
        average_price = group.nlargest(NUM_AVG,'OPI')["Close"].mean()
        OPI = group.nlargest(NUM_AVG,'OPI')["OPI"].mean()
        VOL = group.nlargest(NUM_AVG,'OPI')["Vol"].mean()
        try:
            df = group.nlargest(NUM_AVG,'OPI').sort_values(by=['Maturity'])
            # Roll yield defination here is Ann.(far leg - near leg)/near leg
            roll_yield = df["Close"].pct_change().values[1]*365/df["Maturity"].diff().dt.days.values[1]
        except:
            roll_yield = 0
        tt = {}
        tt["Dates"] = name
        tt["Code"] = code
        tt["Price"] = average_price
        tt["OPI"] = OPI
        tt["Vol"] = VOL
        tt["Roll_Yield"] = roll_yield
        ans.append(tt)
    df = pd.DataFrame(ans)[["Dates","Code","Price","OPI","Vol","Roll_Yield"]].set_index("Dates")
    df["MA55"] = df["Price"].rolling(N).mean()
    return df

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

def regime_p_matrix( df, code, regimes ):
    """ Generate regime probability
        matrix based on dataframe columns 
        note: code named column should be 
            market price to analyze 
            all regimes columns are regime information
        regime defined as 1 long -1 short 0 no trend
        N days averaage +- 1std as the boundary
    """
    N = 55
    new_name = ",".join(regimes)
    for name in df.columns:
        # Get all regime settings
        df[name+"_reg"] = np.where(df[name] >= df[name].rolling(N).mean(),1, -1)
        df[name+"_reg"] = df[name+"_reg"].astype(str)
    df["feature"] = ""
    for reg in regimes:
        df["feature"] += df[reg+"_reg"]+","
    g1 = df.groupby(["feature",code+"_reg"]).agg({code+"_reg": 'count'})
    g2 = df.groupby(["feature"]).agg({code+"_reg": 'count'})
    ans = (g1.div(g2,level="feature")*100).astype(int)
    ans = ans.unstack(level=-1)
    ans = ans.fillna(0)
    ans["NUM"] = g2
    ans.columns = ans.columns.map('|'.join).str.strip('|')
    ans.index.names = [new_name]
    return ans