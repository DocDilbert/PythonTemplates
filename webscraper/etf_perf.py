import json
import pandas as pd
import numpy as np
from datetime import datetime
import argparse
import sys
import csv
import pprint


def perf(data):
    performance = {
        k: v['performance']
        for k, v in data.items()
        if 'performance' in v
    }

    
    print("                   ALL: ", len(performance))
    filter_fuenf = {
        k: v
        for k,v in performance.items()
        if v['fuenf_jahre'] is not None and v['fuenf_jahre'] >= 0.0
    }
    print("                    5a: ", len(filter_fuenf))

    filter_drei = {
        k: v
        for k,v in filter_fuenf.items()
        if v['drei_jahre'] is not None and v['drei_jahre'] >= 0.0
    }

    print("                5a, 3a: ", len(filter_drei))


    filter_ein = {
        k: v
        for k,v in filter_drei.items()
        if v['ein_jahr'] is not None and v['ein_jahr'] >= 0.0
    }

    print("            5a, 3a, 1a: ", len(filter_ein))

    filter_sechsm = {
        k: v
        for k,v in filter_ein.items()
        if v['sechs_monate'] is not None and v['sechs_monate'] >= 0.0
    }

    print("        5a, 3a, 1a, 6m: ", len(filter_sechsm))

    filter_dreim = {
        k: v
        for k,v in filter_sechsm.items()
        if v['drei_monate'] is not None and v['drei_monate'] >= 0.0
    }

    print("    5a, 3a, 1a, 6m, 3m: ", len(filter_dreim))

    filter_einm = {
        k: v
        for k,v in filter_dreim.items()
        if v['ein_monat'] is not None and v['ein_monat'] >= 0.0
    }

    print("5a, 3a, 1a, 6m, 3m, 1m: ", len(filter_einm)) 

    #for isin, i in filter_ein.items():
    #    print(isin, i)


def main():
    parser = argparse.ArgumentParser(
        prog="etf_perf",
    )

    parser.add_argument(
        'operation',
        choices={'perf'},
        help='perf'
    )

    args = parser.parse_args(sys.argv[1:])

    with open("data_stocks/stocks.json", encoding="utf-8") as fp:
        data = json.load(fp)

    if args.operation == "perf":
        perf(data)

    else:
        parser.print_help()
        exit(-1)


if __name__ == "__main__":
    main()