# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 02:52:17 2019

@author: shaolun Du
@contact:Shaolun.du@gmail.com
"""
def get_industry_data_V2( data, relative=False ):
    import Tracker_Central_Dict.industry_dict as I_D
    from stock_currency import cal_stock_index as cal
    dictionary_all = {}
    col_names = ["Chemicals","Metals","Paper","Steel","Architecture","Cars","Cloth","Media","Home_Appliance",
                 "Food","Wine","Beverage","Medicine","Retail","Oil_Gas","Coal","Energy_Facility",
                 "Bank","Insurance","Securities","Financial_Service","Medical","Medical_Service",
                 "Biotechnology","Trans_Port","Trans_Road","Aviation","National_Defense","IT_Hardware",
                 "IT_Software","Communication_Equipment","Tel_Service","Electronic","Elec_Power","Water_Gas",
                 "Urban_Construction","Development","Dividends"]
    for dd in [I_D.MATERIALS,I_D.Consumer_Discretionary,
               I_D.Consumer_Staples,I_D.Energy,I_D.Finance,
               I_D.Medical_Health,I_D.Industry,I_D.Information_Technology,
               I_D.Utilities,I_D.Real_Estate,I_D.Dividend]:
        dictionary_all.update(dd)
    df = cal.get_industry_index(data,dictionary_all,relative)
    df = df[col_names]
    return df