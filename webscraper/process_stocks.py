import json
from datetime import datetime
SESSION_ID = 2


def main():
    with open("data_stocks/stocks_raw.json", encoding="utf-8") as fp:
        raw_data = json.load(fp)

    raw_data_historie = [
        {k: v for k, v in i.items() if k != "type"}
        for _, x in raw_data.items() for i in x
        if i['type'] == 'historie'
    ]

    raw_data_uebersicht = [
        {k: v for k, v in i.items() if k != "type"}
        for _, x in raw_data.items() for i in x
        if i['type'] == "uebersicht"
    ]

    raw_data_profil = [
        {k: v for k, v in i.items() if k != "type"}
        for _, x in raw_data.items() for i in x
        if i['type'] == "profil"
    ]

    isins = set([
        i['isin']
        for _, x in raw_data.items() for i in x
        if 'isin' in i
    ])

    uebersicht = {}
    for i in raw_data_uebersicht:
        isin = i['isin']

        entry = uebersicht.setdefault(isin, {})
        entry.update({
            "name": i['name'],
            "wkn": i['wkn'],
            "waehrung": i['waehrung']
        })

    profil = {}
    for i in raw_data_profil:
        isin = i['isin']
        guv = i['guv']
        guv_header = guv['header'][1:]
        guv_data = guv['data']

        guv_jahresueberschuss = next(
            x[1:] 
            for x in guv_data 
            if len(x)>=1 and "Jahresüberschuss" in x[0]
        )
        guv_jahresueberschuss = [
            float(x.replace('.','').replace(',','.'))
            for x in guv_jahresueberschuss
        ]

        guv_jahresueberschuss = [
            [k , v] 
            for k, v in zip(guv_header, guv_jahresueberschuss)
        ]

        entry = profil.setdefault(isin, {})
        entry.update({
            "wkn": i['wkn'],
            "guv" : {
                "jahresueberschuss" : guv_jahresueberschuss[::-1]
            }
        })

    historie = {}
    for h in raw_data_historie:
        isin = h['isin']

        
        entry = historie.setdefault(isin, [])
        for i in h['historie']:
            entry.append(i)

    data_per_isin = {}
    for isin in isins:

        # isolate entries
        try:
            k = {i['datum']: i for i in historie[isin]}
        except KeyError:
            print("Missing history: "+isin)
            continue

        # combine and sort
        historie_dict = sorted(
            list(k.values()),
            key=lambda x: datetime.strptime(
                x['datum'], '%d.%m.%Y')
        )

        historie_list = [
            [x['datum'], x['eroeffnung'], x['schlusskurs'], x['hoch'], x['tief']]
            for x in historie_dict
        ]

        try:
            ueberischt_of_isin = uebersicht[isin]
        except KeyError:
            print("Missing overview: "+isin)
            continue

        try:
            profil_of_isin = profil[isin]
        except KeyError:
            print("Missing profile: "+isin)
            continue

        data_per_isin[isin] = {
            "historie": historie_list
        }

        data_per_isin[isin].update(
            profil_of_isin
        )

        data_per_isin[isin].update(
            ueberischt_of_isin
        )


    with open("data_stocks/stocks.json", "w", encoding="utf-8") as fp:
        json.dump(data_per_isin, fp, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
