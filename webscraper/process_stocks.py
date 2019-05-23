import json
from datetime import datetime
def main():
    with open("data_stocks/stocks_raw.json", encoding="utf-8") as fp:
        raw_data = json.load(fp)

    
    data = [
        i
        for _, x in raw_data.items() for i in x 
        if i['type'] == 'historie'
    ]

    isins={}
    for h in data:
        isin = h['isin']

        if isin not in isins:
            isins[isin] = []

        for i in h['historie']:
            isins[isin].append(i)

    data_per_isin = {}
    for isin, history in isins.items():
        k = {i['datum'] : i for i in history}
        data_per_isin[isin] = {
            "historie" : sorted(list(k.values()), 
                    key=lambda x:datetime.strptime( x['datum'], '%d.%m.%Y')
                )

        }
    with open("data_stocks/stocks.json", "w", encoding="utf-8") as fp:
        json.dump(data_per_isin, fp, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()