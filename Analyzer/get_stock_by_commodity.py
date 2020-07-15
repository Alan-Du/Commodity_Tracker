# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 05:50:43 2020
Get single stock sector dataframe
@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
import stock_currency.stock_handler as s_handler
import stock_currency.get_stock_sector_index as stock_sector

def get_stock_by_commodity( start, end, commodity_ticker ):
    handler = s_handler.stock_handler()
    stock_data_all = handler._gen_all_ticker_df(start,end)
    i_dict = stock_sector.industry_lookup(commodity_ticker)
    s_dict = i_dict["PRODUCER"]
    index_dict = i_dict["ShangHai_Index"]
    data = stock_data_all[s_dict[0]]/stock_data_all[s_dict[0]].iloc[0]
    data[commodity_ticker+"_Stock"] = data.apply(lambda x: sum(x[s_dict[0]]*s_dict[1]),axis=1)
    data_index = stock_data_all[index_dict[0]]/stock_data_all[index_dict[0]].iloc[0]
    data["Index_Stock"] = data_index.apply(lambda x: sum(x[index_dict[0]]*index_dict[1]),axis=1)
    return data[[commodity_ticker+"_Stock","Index_Stock"]]

if __name__ == "__main__":
    import datetime as dt
    start = dt.datetime(2019, 1, 1).date()
    end = dt.date.today()
    data = get_stock_by_commodity(start,end,"AU")
    data.plot()
    print(data)

