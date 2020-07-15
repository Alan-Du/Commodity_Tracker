""" Update memo 10/15/2019
    auto update currency price into local database
"""
def gen_weekly_ccy_df( start,end ):
    from DB.fetch import get_histroical_ccy
    import pandas as pd
    """ Generate weekly ccy data table
    """
    currency_li =[ "USD_Index",
                   "EURUSD","GBPUSD","AUDUSD","CADUSD",
                   "JPYUSD",
                   "CNYUSD","HKDUSD","TWDUSD",
                   "KRWUSD","THBUSD","SGDUSD","MYRUSD",
                   "BRLUSD","INRUSD",
                   "CNY_raw","JPY_raw",
                   "WTI"
                  ]
    currency_df = pd.DataFrame(get_histroical_ccy(start,end)).set_index("Dates")
    temp = currency_df[["JPYUSD","CNYUSD"]]
    currency_df["EURUSD"] = 1/currency_df["USDEUR"]
    currency_df["GBPUSD"] = 1/currency_df["USDGBP"]
    currency_df["AUDUSD"] = 1/currency_df["USDAUD"]
    currency_df = currency_df/currency_df.iloc[0]
    currency_df["CNY_raw"] = temp["CNYUSD"]
    currency_df["JPY_raw"] = temp["JPYUSD"]
    return currency_df[currency_li],currency_li
    

