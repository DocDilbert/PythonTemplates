import json
from datetime import datetime
SESSION_ID = 2
def main():
    with open("data_stocks/stocks_raw.json", encoding="utf-8") as fp:
        raw_data = json.load(fp)

    
    data_historie = [
        i
        for _, x in raw_data.items() for i in x 
        if i['type'] == 'historie'
    ]

    data_uebersicht = [
        {k:v for k, v in i.items() if k != "type"} 
        for _, x in raw_data.items()  for i in x
        if i['type']=="uebersicht"
    ]

    uebersicht={}
    for i in data_uebersicht:
        isin = i['isin']

        entry = uebersicht.setdefault(isin, {})
        entry.update({
            "name":i['name'],
            "wkn":i['wkn'],
            "waehrung":i['waehrung']
        })
        
    historie={}
    for h in data_historie:
        isin = h['isin']

        entry = historie.setdefault(isin, [])
        for i in h['historie']:
            entry.append(i)

    data_per_isin = {}
    for isin, history in historie.items():
        k = {i['datum'] : i for i in history}

        historie_dict = sorted(list(k.values()), 
            key=lambda x:datetime.strptime( x['datum'], '%d.%m.%Y')
        )

        historie_list = [
            [x['datum'], x['eroeffnung'],x['schlusskurs'], x['hoch'], x['tief']]
            for x in historie_dict
        ]

        data_per_isin[isin] = {
            "historie" : historie_list
        }
        
        data_per_isin[isin].update(
            uebersicht[isin]
        )

    with open("data_stocks/stocks.json", "w", encoding="utf-8") as fp:
        json.dump(data_per_isin, fp, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()