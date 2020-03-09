"""
Created on Sun Sep 22 08:24:36 2019

@author: shaolun du
@contact: Shaolun.du@gmail.com

Structure outline:
    HTML page with pandas read html parser
"""
import requests
def ZZ_proc_params(start_date_str, end_date_str):
    import datetime,re
    def check_date_format(date_str):
        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            return True
        else:
            return False
    date_list = []
    if check_date_format(start_date_str) and \
        check_date_format(end_date_str):
        year_start, month_start, day_start = start_date_str.split("-")
        year_end, month_end, day_end = end_date_str.split("-")
        start_date = datetime.date(int(year_start),
                                   int(month_start),
                                   int(day_start))
        end_date = datetime.date(int(year_end),
                                 int(month_end),
                                 int(day_end))
        delta_days = (end_date-start_date).days
        i = 0
        if delta_days>=0:
            while i <= delta_days:
                date = start_date+datetime.timedelta(days=i)
                date_list.append([date.strftime('%Y'),date.strftime('%Y%m%d')])
                i += 1
            return date_list
        else:
            print("input params end_date is earlier than start_date")
            raise
    else:
        return None

class ZZ_parser:
    def __init__( self ):
        self.URL_TEMPL = "http://www.czce.com.cn/cn/DFSStaticFiles/Future/{}/{}/FutureDataDaily.htm"
        self.col_names = ["Dates","Code","Open","High","Low","Close","OPI","Vol"]
        self.datas     = []
    def download(self,sdate,edate):
        print("Exchange ZZ--->")
        # Start downloading given period
        import pandas as pd
        dates_li = ZZ_proc_params(sdate,edate)
        ans = pd.DataFrame()
        with requests.Session() as s:
            for dates in dates_li:
                print(dates)
                url = self.URL_TEMPL.format(dates[0],dates[1])
                try:
                    page = s.get(url).text
                    if int(dates[0]) <2018:
                        df = pd.read_html(page,skiprows=1,attrs={"id":"senfe"})[0]
                    else:
                        df = pd.read_html(page,skiprows=0)[0]
                except:
                    continue
                df.columns = [i for i in range(14)]
                df["Dates"] = dates[1]
                df = df[["Dates",0,2,3,4,5,10,9]]
                df.columns = self.col_names
                df = df.dropna()
                ans = ans.append(df)
        self.datas = ans
            
    def get_data_df(self):
        return self.datas
