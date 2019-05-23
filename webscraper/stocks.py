import json
import pprint
import numpy as np
import matplotlib.pyplot as plt
SESSION_ID = 1
def test1():
    with open("data_stocks/stocks_raw.json", encoding="utf-8") as fp:
        raw_data = json.load(fp)
 
    #pprint.pprint(historie)

    uebersicht = [
        {k:v for k, v in x.items() if k != "type"} 
        for x in raw_data[str(SESSION_ID)] 
        if x['type']=="uebersicht"
    ]

    aktien_uebersicht = [
        {k:v for k, v in x.items() if k != "gattung"} 
        for x in uebersicht
        if x['gattung']=="Aktie"
    ]
    
    branchen = list({
        x['branche'] for x in aktien_uebersicht
    })
    pprint.pprint(branchen)
    branche = "Telekomm."
    aktien_uebersicht_per_branche = [
        {k:v for k, v in x.items() if k != "gattung"} 
        for x in uebersicht
        if (x['gattung']=="Aktie") and (x['branche'] == branche)
    ]

    isin = [x['isin'] for x in aktien_uebersicht_per_branche]
    aktueller_kurs = [x['kurse']['aktueller_kurs'] for x in aktien_uebersicht_per_branche]
    tageshoch = [x['kurse']['tageshoch'] for x in aktien_uebersicht_per_branche]
    tagestief = [x['kurse']['tagestief'] for x in aktien_uebersicht_per_branche]
    wochenhoch = [x['kurse']['wochenhoch'] for x in aktien_uebersicht_per_branche]
    wochentief = [x['kurse']['wochentief'] for x in aktien_uebersicht_per_branche]

    aktueller_kurs, tageshoch, tagestief, wochentief, wochenhoch, isin = zip(*sorted(zip(aktueller_kurs, tageshoch, tagestief,wochentief,wochenhoch, isin)))

    width = 0.5       # the width of the bars: can also be len(x) sequence
    plt.rcdefaults()    

    fig, ax = plt.subplots()
    fig.subplots_adjust(
        left = 0.1,
        right= 0.95,
        bottom = 0.2,
        top = 0.93
    )
    x_pos = np.arange(len(isin))
    
    ax.bar(x_pos, [wh-wt for wh, wt in zip(wochenhoch, wochentief)], width, bottom=wochentief)
    ax.bar(x_pos, [th-tt for th, tt in zip(tageshoch, tagestief)], width*1.5, bottom=tagestief)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(isin, rotation='vertical')


    #ax.boxplot([(x,y,z)
    #    for x,y,z in zip(x_pos, wochenhoch, wochentief)
#
    #])
    #ax.set_yscale("log", nonposy='clip')
    plt.title(branche)
    plt.show()
def test2():
    with open("data_stocks/stocks_raw.json", encoding="utf-8") as fp:
        raw_data = json.load(fp)
 
    #pprint.pprint(historie)

    uebersicht = [
        {k:v for k, v in x.items() if k != "type"} 
        for x in raw_data[str(SESSION_ID)] 
        if x['type']=="uebersicht"
    ]

    aktien_uebersicht = [
        {k:v for k, v in x.items() if k != "gattung"} 
        for x in uebersicht
        if x['gattung']=="Aktie"
    ]

    perf_pa = 6
    performance_1a_pos = {x['isin']:x
        for x in uebersicht
        if (x['performance']['drei_jahre'] is not None and x['performance']['drei_jahre']>=perf_pa*3.0) and
           (x['performance']['ein_jahr'] is not None and x['performance']['ein_jahr']>=perf_pa) and
           (x['performance']['sechs_monate'] is not None and x['performance']['sechs_monate']>=perf_pa*0.5) and
           (x['performance']['drei_monate'] is not None and x['performance']['drei_monate']>=perf_pa*0.5*0.5) and
           (x['performance']['ein_monat'] is not None and x['performance']['ein_monat']>=perf_pa*0.5*0.5*0.33333) 
    }

    for _,x in performance_1a_pos.items():
        print(
            x['isin'], 
            x['performance']['drei_jahre'],
            x['performance']['ein_jahr'], 
            x['performance']['sechs_monate'],
            x['performance']['drei_monate'],
            x['performance']['ein_monat'],
            x['name'])

if __name__ == "__main__":
    #test1()
    test2()