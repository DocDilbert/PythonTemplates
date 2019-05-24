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

    parser = argparse.ArgumentParser(
        prog="plot_stock",
    )
    
    parser.add_argument(
        'isin',
        help='isin to plot',
        type=str
    )
    args = parser.parse_args(sys.argv[1:])

    with open("data_stocks/stocks.json", encoding="utf-8") as fp:
        data = json.load(fp)
    
    stock = data[args.isin]
    name = stock['name']
    historie = [ [date2num(datetime.strptime(x[0], '%d.%m.%Y'))]+x[1:5] for x in stock['historie']]


    fig, ax = plt.subplots()
    weekFormatter = DateFormatter('%b %d, %Y')
    ax.xaxis.set_major_formatter(weekFormatter)
    candlestick_ochl(ax, historie,colorup='g', colordown='r',)
    plt.title(name)
    plt.show()


if __name__ == "__main__":
    main()