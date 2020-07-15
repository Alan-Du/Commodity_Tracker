# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 22:02:36 2020

@author: shaolun du
@contact: shaolun.du@gmail.com
"""
def combin_current_data( current,
                         start_date,
                         end_date ):
    import pandas as pd
    data = pd.DataFrame()
    for cc in current:
        df = pd.read_excel(cc)[["Code","Dates","OPI","Close"]]
        df["Dates"] = df["Dates"].apply(lambda x: pd.to_datetime(str(x),errors="coerce"))
        mask = (df["Dates"] >= start_date) & (df["Dates"] <= end_date)
        df = df.loc[mask]
        df['OPI'] = df['OPI'].astype(str).str.replace(",","").astype(float)
        df['Close'] = df['Close'].astype(str).str.replace(",","").astype(float)
        data = data.append(df)
    return data

