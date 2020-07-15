# -*- coding: utf-8 -*-    
def set_sector_weights():
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



