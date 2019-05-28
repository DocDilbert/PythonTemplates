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
import csv
import pprint


def sorted_key(x, l):
    criteria = []

    for i in reversed(range(l)):
        criteria.append(
            (1.0 if x[i+1][1] >= 0.0 else -1.0)
            if (x[i+1][1] is not None) else -float('inf'))

    for i in range(l):
        criteria.append(
            x[i+1][1]
            if (x[i+1][1] is not None) else -float('inf'))

    
    return criteria


def diff(data, group, value):

    eval_value = {
        k: v[group][value]
        for k, v in data.items()
        if v[group][value] is not None
    }

    years = set()
    for isin, value in eval_value.items():

        for i in value:
            years.add(i[0])

    years = sorted(list(years))

    last_year = years[0]

    from_to = []
    for year in years[1:]:
        from_to.append((last_year, year))
        last_year = year

    data_over_isin = {}

    for isin, value in eval_value.items():

        p_list = []

        for f, t in from_to:
            f_i = next((i for i in value if i[0] == f), None)
            t_i = next((i for i in value if i[0] == t), None)

            if f_i is None or t_i is None:
                p_list.append(["{}->{}".format(f, t), None])
            else:
                try:
                    perc = (t_i[1]/f_i[1] - 1.0)*100
                except TypeError:
                    p_list.append(["{}->{}".format(f, t), None])
                except ZeroDivisionError:
                    p_list.append(["{}->{}".format(f, t), None])
                else:
                    p_list.append(["{}->{}".format(f, t), perc])

        data_over_isin[isin] = p_list

    data_sorted = sorted(
        (
            [isin] + data
            for isin, data in data_over_isin.items()
        ),
        key=lambda x: sorted_key(x, len(from_to))
    )

    with open('results.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='"', quoting=csv.QUOTE_MINIMAL)

        headers = ['isin']

        for f, t in from_to:
            headers.append("{} -> {}".format(f, t))

        csvwriter.writerow(headers)

        for data in data_sorted:

            isin = data[0]
            row = [x[1] for x in data[1:]]
            csvwriter.writerow(
                [isin] + list(map(
                    lambda x: "{:.3f}".format(x) if x is not None else "",
                    row
                ))
            )


def abs(data, op, group, value):

    eval_value = {
        k: v[group][value]
        for k, v in data.items()
        if v[group][value] is not None
    }

    years = set()
    for isin, value in eval_value.items():

        for i in value:
            years.add(i[0])

    years = sorted(list(years))

    data_over_isin = {}

    for isin, value in eval_value.items():

        p_list = []

        for year in years:
            try:
                i = next(
                    (
                        [i[0]] + [op(data[isin],l) for l in i[1:]] 
                        for i in value if i[0] == year
                    ), 
                    None
                )
            except ZeroDivisionError:
                i = None

            if i is None:
                p_list.append(["{}".format(year), None])
            else:
                p_list.append(i)

        data_over_isin[isin] = p_list

    data_sorted = sorted(
        (
            [isin] + data
            for isin, data in data_over_isin.items()
        ),
        key=lambda x: sorted_key(x, len(years))
    )


    with open('results.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='"', quoting=csv.QUOTE_MINIMAL)

        headers = ['isin']

        for year in years:
            headers.append("{}".format(year))

        csvwriter.writerow(headers)

        for data in data_sorted:

            isin = data[0]
            row = [x[1] for x in data[1:]]
            csvwriter.writerow(
                [isin] + list(map(
                    lambda x: "{:.3f}".format(x) if x is not None else "",
                    row
                ))
            )


def main():
    parser = argparse.ArgumentParser(
        prog="eval_stocks",
    )
    
    parser.add_argument(
        'operation',
        help='abs, diff'
    )

    parser.add_argument(
        'group',
        help='name of group to evaluate',
        type=str
    )
    parser.add_argument(
        'value',
        help='name of value to evaluate',
        type=str
    )
    args = parser.parse_args(sys.argv[1:])

    with open("data_stocks/stocks.json", encoding="utf-8") as fp:
        data = json.load(fp)

    if args.operation=="diff":
        diff(data, args.group, args.value)
    elif args.operation=="abs":
        abs(
            data, 
            lambda e, x:x, 
            args.group, 
            args.value
        )
    elif args.operation=="kgx":
        abs(
            data, 
            lambda e, x:e['kurse']['aktueller_kurs']/x if x!=None else None, 
            'wertpapierdaten', 
            'gewinn_je_aktie'
        )

    elif args.operation=="divren":
        abs(
            data, 
            lambda e, x:(x*100)/e['kurse']['aktueller_kurs'] if x!=None else None, 
            'wertpapierdaten', 
            'dividende_je_aktie'
        )
    else:
        parser.print_help()
        exit(-1)

if __name__ == "__main__":
    main()
