"""
Created on Sun Sep 22 08:24:36 2019

@author: shaolun du
@contact: Shaolun.du@gmail.com

Structure outline:
    HTML page with pandas read html parser
"""
import requests
def dl_proc_params(start_date_str, end_date_str):
    import re
    import datetime
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
                date_list.append([int(date.strftime('%Y')),int(date.strftime('%m'))-1,int(date.strftime('%d'))])
                i += 1
            return date_list
        else:
            print("input params end_date is earlier than start_date")
            raise
    else:
        return None
    
class DL_parser:
    def __init__( self ):
        self.URL_TEMPL = "http://www.dce.com.cn/publicweb/quotesdata/dayQuotesCh.html"
        self.headers   = { 'Content-Type': 'application/x-www-form-urlencoded',
                           'Cookie': 'JSESSIONID=34581314E8E6F047ABE7D22180DCE3A2; WMONID=-b8uBX4vHDi; Hm_lvt_a50228174de2a93aee654389576b60fb=1567732473,1568333912,1568936184,1569113640; Hm_lpvt_a50228174de2a93aee654389576b60fb=1569113660',
                           'Referer': 'http://www.dce.com.cn/publicweb/quotesdata/dayQuotesCh.html',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
                         }
        self.payload = { 'dayQuotes.variety': 'all',
                         'dayQuotes.trade_type': '0',
                         'year': 0,
                         'month':0,
                         'day':  0,
                       }
        self.col_names = ["Dates","Code","Open","High","Low","Close","OPI","Vol"]
        self.name_map  = {"豆一":"a","豆二":"b","乙二醇":"eg","焦煤":"jm","焦炭":"j",
                          "铁矿石":"i","聚氯乙烯":"pvc","聚丙烯":"pp","聚乙烯":"pe","豆粕":"m",
                          "豆油":"y","棕榈油":"p","鸡蛋":"jd","玉米淀粉":"cs","玉米":"c"}
        self.datas     = []
    def download(self,sdate,edate):
        # Start downloading given period
        print("Exchange DL--->")
        import pandas as pd
        dates_li = dl_proc_params(sdate,edate)
        ans = pd.DataFrame()
        with requests.Session() as s:
            for dates in dates_li:
                print(dates)
                self.payload['year'] = dates[0]
                self.payload['month'] = dates[1]
                self.payload['day'] = dates[2]
                page = s.post( self.URL_TEMPL, data=self.payload, headers=self.headers).text
                try:
                    df = pd.read_html(page,skiprows=0)[0]
                except:
                    continue
                df.iloc[:,0] = df.iloc[:,0].map(self.name_map)
                df = df.dropna()
                df["Dates"] = str(dates[0])+"{:02d}".format(dates[1]+1)+"{:02d}".format(dates[2])
                df["Code"]  = df.iloc[:,0]+df.iloc[:,1].astype(int).astype(str)
                df["Open"] = df.iloc[:,2]
                df["High"] = df.iloc[:,3]
                df["Low"] = df.iloc[:,4]
                df["Close"] = df.iloc[:,5]
                df["OPI"] = df.iloc[:,11]
                df["Vol"] = df.iloc[:,10]
                df = df[["Dates","Code","Open","High","Low","Close","OPI","Vol"]]
                ans = ans.append(df)
        self.datas = ans
            
    def get_data_df(self):
        return self.datas
