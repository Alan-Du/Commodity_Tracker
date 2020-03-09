# -*- coding: utf-8 -*-

def wavg(group, avg_name, weight_name):
    """ http://stackoverflow.com/questions/10951341/pandas-dataframe-aggregate-function-using-multiple-columns
    In rare instance, we may not have weights, so just return the mean. Customize this if your business case
    should return otherwise.
    """
    d = group[avg_name]
    w = group[weight_name]
    try:
        return (d * w).sum() / w.sum()
    except ZeroDivisionError:
        return d.mean()


def get_sector_weights():
    metal = ["AG","AU","CU","AL","ZN","PB","NI","SN"]
    metal_weights = [ 0, 0, 0.3, 0.3, 0.1, 0.1, 0.1, 0.1]
    bk = ["ZC","JM","J","I","RB","HC","FG"]
    bk_weights = [ 0.2, 0.1, 0.1, 0.2, 0.1, 0.1, 0.2 ]
    chem = ["TA","PVC","PP","PE","RU","BU","MA"]
    chem_weights = [ 0.2, 0.1, 0.1, 0.1, 0.2, 0.2,0.1 ]
    agri = ["A","M","RM","Y","OI","P","SR","CF","JD","CS","C"]
    agri_weights = [ 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
                     0.1, 0.1, 0.05, 0.05, 0.1]
    stock = ["IC","IF","IH"]
    stock_weights = [ 0.4,0.3,0.3]
    bond = ["T","TF","TS"]
    bond_weights = [0.4,0.3,0.3]
    return [ [metal,"Metal",metal_weights],[bk,"Black_Cons",bk_weights],
             [chem,"Chemistry",chem_weights],[agri,"Agriculture",agri_weights],
             [stock,"Stock",stock_weights], [bond,"Bond",bond_weights] ]
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


