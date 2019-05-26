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

def main():

    with open("data_stocks/stocks.json", encoding="utf-8") as fp:
        data = json.load(fp)
    
    jahresueberschuss = {
        k:v['guv']['jahresueberschuss']
        for k,v in data.items()
    }

    for isin, value in jahresueberschuss.items():
        last_entry = value[0]
    
        buf = []
        for entry in value[1:]:
            perc = (entry[1]/last_entry[1] - 1.0)*100
            buf.append(("{} -> {} = {:<+7.1f}".format(last_entry[0], entry[0], perc)))
            last_entry = entry
            
        print(isin+" ---- " +" / ".join(buf))

if __name__ == "__main__":
    main()