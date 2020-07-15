# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 21:56:55 2020
This is date list generator for all exchanges url format
@author: shaolun du
@contact: shaolun.du@gmail.com
"""
import datetime,re
def gen_proc_params(exc, start_date_str, end_date_str):
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
                if exc == "ZZ":
                    date_list.append([date.strftime('%Y'),date.strftime('%Y%m%d')])
                elif exc == "SH":
                    date_list.append(date.strftime('%Y%m%d'))
                elif exc == "DL":
                    date_list.append([int(date.strftime('%Y')),int(date.strftime('%m'))-1,int(date.strftime('%d')),date])
                elif exc == "ZJ":
                    date_list.append([date.strftime('%Y%m'),date.strftime('%d')])
                elif exc == "SH_inv":
                    date_list.append([date.strftime("%Y"),date.strftime('%Y%m%d'),date])
                else:
                    print("Exchange code:{} error".format(exc))
                    raise
                i += 1
            return date_list
        else:
            print("input params end date is earlier than start_date")
            raise
    else:
        print("Date format incorrect. Should be yyyy-mm-dd.")
        raise

