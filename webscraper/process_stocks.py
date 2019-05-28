import json
import pprint
from datetime import datetime
SESSION_ID = 2


def isolate_profile_value(items, group, name):

    header = [l for i in items for l in i[group]['header'][1:]]
    data = [l for i in items for l in i[group]['data']]
    has_quantifier = ['quantifier' in i[group] for i in items ][-1]

    quantifier = 1
    if has_quantifier:
        quantifier_str = [i[group]['quantifier'] for i in items ][-1]
        if quantifier_str == 'Mio':
            quantifier=1000000
        else:
            raise ValueError
    
    #has_currency = ['currency' in i[group] for i in items ][-1]
    #currency = None
    #if has_currency:
    #    currency = [i[group]['currency'] for i in items ][-1]

    # Neue sessions überschreiben ältere. So ist alles aktuell
    isolated = [
        {key: i for key, i in zip(header, x[1:])}
        for x in data
        if len(x) >= 1 and name in x[0]
    ]

    if len(isolated) == 0:
        return None

    isolated = {
        k: quantifier*float(x.replace('.', '').replace(',', '.')) if x != "-" else None
        for i in isolated
        for k, x in i.items()
    }

    isolated = sorted([
        [k, v]
        for k, v in isolated.items()
    ])

    return isolated


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
            "waehrung": i['waehrung'],
            "kurse":{
                'aktueller_kurs' : i['kurse']["aktueller_kurs"]
            }
        })

    raw_data_profil_by_isin = {
        isin: [x for x in raw_data_profil if x['isin'] == isin]
        for isin in isins
    }

    profil_by_isin = {}
    for isin, profile in raw_data_profil_by_isin.items():
        if len(profile) == 0:
            continue

        entry = profil_by_isin.setdefault(isin, {})

        

        entry.update({
            "wkn": i['wkn'],
            "guv": {
                "jahresueberschuss": isolate_profile_value(profile, 'guv', 'Jahresüberschuss')
            },
            "wertpapierdaten": {
                "gewinn_je_aktie": isolate_profile_value(profile, 'wertpapierdaten', 'Gewinn je Aktie'),
                "ergebnis_je_aktie_verwässert": isolate_profile_value(profile,'wertpapierdaten', "Ergebnis je Aktie verwässert"),
                "dividende_je_aktie": isolate_profile_value(profile, 'wertpapierdaten', 'Dividende je Aktie'),
                "dividende": isolate_profile_value(profile, 'wertpapierdaten', 'Dividende')
            },
            "bilanz": {
                "aktiva": {
                    "summe_umlaufvermögen": isolate_profile_value(profile, 'bilanz', 'Summe Umlaufvermögen')
                }
            },
            "bewertungszahlen" : {
                "umsatz_je_aktie" : isolate_profile_value(profile, 'bewertungszahlen', "Umsatz je Aktie"),
                "cashflow_je_aktie" : isolate_profile_value(profile, 'bewertungszahlen', "Cashflow je Aktie"),
                "fremdkapitalquote" : isolate_profile_value(profile, 'bewertungszahlen', "Fremdkapitalquote")
            },
            "mitarbeiter": {
                "anzahl_der_mitarbeiter" : isolate_profile_value(profile, 'mitarbeiter', 'Anzahl der Mitarbeiter')
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
        history_dict = sorted(
            list(k.values()),
            key=lambda x: datetime.strptime(
                x['datum'], '%d.%m.%Y')
        )

        history_list = [
            [x['datum'], x['eroeffnung'], x['schlusskurs'], x['hoch'], x['tief']]
            for x in history_dict
        ]

        try:
            ueberischt_of_isin = uebersicht[isin]
        except KeyError:
            print("Missing overview: "+isin)
            continue

        try:
            profil_of_isin = profil_by_isin[isin]
        except KeyError:
            print("Missing profile: "+isin)
            continue

        data_per_isin[isin] = {
            "historie": history_list
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
