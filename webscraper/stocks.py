import json
import pprint
import numpy as np
import matplotlib.pyplot as plt
SESSION_ID = 1
def main():
    with open("data_dax/boerse_raw.json", encoding="utf-8") as fp:
        raw_data = json.load(fp)

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
    

    isin = [x['isin'] for x in aktien_uebersicht]
    kurs = [x['kurse']['aktueller_kurs'] for x in aktien_uebersicht]
    wochenhoch = [x['kurse']['wochenhoch'] for x in aktien_uebersicht]
    wochentief = [x['kurse']['wochentief'] for x in aktien_uebersicht]

    kurs, wochentief, wochenhoch, isin = zip(*sorted(zip(kurs,wochentief,wochenhoch, isin)))

    width = 0.5       # the width of the bars: can also be len(x) sequence
    plt.rcdefaults()    

    fig, ax = plt.subplots()
    fig.subplots_adjust(
        left = 0.1,
        right= 0.95,
        bottom = 0.2,
        top = 0.95
    )
    x_pos = np.arange(len(isin))
    ax.bar(x_pos, wochenhoch, width, bottom=wochentief)
    ax.plot(x_pos,kurs, 'rx')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(isin, rotation='vertical')
    #ax.boxplot([(x,y,z)
    #    for x,y,z in zip(x_pos, wochenhoch, wochentief)
#
    #])
    ax.set_yscale("log", nonposy='clip')
    
    plt.show()

if __name__ == "__main__":
    main()