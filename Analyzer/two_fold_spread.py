# -*- coding: utf-8 -*-
"""
Created on Thu May 14 23:59:17 2020
Get all possible two combinations of products spreads
@author: shaolun du
@contact: shaolun.du@gmail.com
"""

def gen_two_fold_spread():
    import DB.fetch as fetch
    import pandas as pd
    from itertools import combinations
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    myFmt = mdates.DateFormatter('%y/%m') # Dates format
    threshold = 0.1
    index_data = pd.DataFrame(fetch.get_index_all()).set_index("Dates")
    metals = ["AG","AU","CU","AL","ZN","PB","NI","SN"]
    construction = ["ZC","JM","J","I","RB","HC","FG"]
    chemical = ["TA","PVC","PP","PE","RU","BU","MA"]
    agricultural = ["A","M","RM","Y","OI","P","SR","CF","CS","C"]
    financial = ["IF","T"]
    for sector in [metals,construction,chemical,agricultural,financial]:
        comb = combinations(sector, 2)
        for pair in list(comb): 
            leg1 = index_data[index_data["name"]==pair[0]]
            leg2 = index_data[index_data["name"]==pair[1]]
            start_date = min(list(set(leg1.index) & set(leg2.index)))
            leg1 = leg1[start_date:]
            leg2 = leg2[start_date:]
            leg1["mid"] = (leg1["open"]+leg1["close"])/2
            leg1["mid"] = leg1["mid"]/leg1["mid"].loc[start_date]
            leg2["mid"] = (leg2["open"]+leg2["close"])/2
            leg2["mid"] = leg2["mid"]/leg2["mid"].loc[start_date]
            spread_name = pair[0]+"_"+pair[1]+"_Spread"
            leg1[spread_name] = leg1["mid"]-leg2["mid"]
            pct_rank = leg1[spread_name].sort_values().values.searchsorted(leg1[spread_name][-1])/len(leg1[spread_name])
            if pct_rank >= (1-threshold) or pct_rank <= threshold:
                fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(8,4))
                axes[0].plot(leg1[spread_name],color='C0', label=spread_name)
                axes[0].legend()
                axes[0].xaxis.set_major_formatter(myFmt)
                axes[1].hist(leg1[spread_name],bins=50,color='C1', label=spread_name)
                axes[1].axvline(leg1[spread_name][-1], color='k', linestyle='dashed', linewidth=3)
                bottom, top = axes[1].get_ylim()
                axes[1].text(leg1[spread_name][-1], top*0.9, 'Current:{:.1},\nPct:{:.1%}'.format(leg1[spread_name][-1],pct_rank))
                fig.autofmt_xdate()
                plt.tight_layout()
                plt.show()
                plt.close(fig)
    return 0

gen_two_fold_spread()
        