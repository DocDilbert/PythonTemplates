import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from mpl_finance import candlestick_ochl
import argparse
import sys

def sorted_key(x, l):
    criteria= []
    for i in reversed(range(l)):
        criteria.append(
            (1 if x[i+1][1]>=0 else -1) 
            if (x[i+1][1] is not None) else -float('inf'))
    for i in range(l):
        criteria.append(
            x[i+1][1] 
            if (x[i+1][1] is not None) else -float('inf'))
    return criteria
def main():

    with open("data_stocks/stocks.json", encoding="utf-8") as fp:
        data = json.load(fp)
    
    jahresueberschuss = {
        k:v['guv']['jahresueberschuss']
        for k,v in data.items()
    }

    years=set()
    for isin, value in jahresueberschuss.items():

        for i in value:
            years.add(i[0])

    years= sorted(list(years))
    
    last_year = years[0]
    from_to = []
    for year in years[1:]:
        from_to.append((last_year, year))
        last_year = year



    data_over_isin = {}
    for isin, value in jahresueberschuss.items():

        p_list = []
        
        for f, t in from_to:
            f_i = next((i for i in value if i[0]==f), None) 
            t_i = next((i for i in value if i[0]==t), None) 

            if f_i is None or t_i is None:
                p_list.append(["{}->{}".format(f,t),None] ) 
            else:
                perc = (t_i[1]/f_i[1] - 1.0)*100
                p_list.append(["{}->{}".format(f,t),perc] ) 
         
        
        data_over_isin[isin] = p_list

    data_sorted = sorted(
        (
            [isin] +  data
            for isin, data in data_over_isin.items()
        ),
        key=lambda x:sorted_key(x, len(from_to))
    )
    import csv
    with open('results.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        headers=['isin']
        for f, t in from_to:
            headers.append("{} -> {}".format(f,t ))

        csvwriter.writerow(headers)
        for data in data_sorted:
   
            isin = data[0]
            row = [x[1] for x in data[1:]]
            csvwriter.writerow(
                [isin] + list(map(
                    lambda x:"{:.3f}".format(x) if x is not None else "",
                    row
                ))
            )

if __name__ == "__main__":
    main()