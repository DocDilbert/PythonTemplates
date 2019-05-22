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
    
    branchen = list({
        x['branche'] for x in aktien_uebersicht
    })
    pprint.pprint(branchen)
    branche = "Dienstlstg."
    aktien_uebersicht_per_branche = [
        {k:v for k, v in x.items() if k != "gattung"} 
        for x in uebersicht
        if (x['gattung']=="Aktie") and (x['branche'] == branche)
    ]

    isin = [x['isin'] for x in aktien_uebersicht_per_branche]
    tageshoch = [x['kurse']['tageshoch'] for x in aktien_uebersicht_per_branche]
    tagestief = [x['kurse']['tagestief'] for x in aktien_uebersicht_per_branche]
    wochenhoch = [x['kurse']['wochenhoch'] for x in aktien_uebersicht_per_branche]
    wochentief = [x['kurse']['wochentief'] for x in aktien_uebersicht_per_branche]

    tageshoch, tagestief, wochentief, wochenhoch, isin = zip(*sorted(zip(tageshoch, tagestief,wochentief,wochenhoch, isin)))

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
    ax.bar(x_pos, [th-tt for th, tt in zip(tageshoch, tagestief)], 0.75, bottom=tagestief)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(isin, rotation='vertical')
    #ax.boxplot([(x,y,z)
    #    for x,y,z in zip(x_pos, wochenhoch, wochentief)
#
    #])
    ax.set_yscale("log", nonposy='clip')
    plt.title(branche)
    plt.show()

if __name__ == "__main__":
    main()