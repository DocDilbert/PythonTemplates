
import datetime
import locale
import requests
import bs4
import dateutil.relativedelta as rd
import numpy as np
import json
import os

# chrome 70.0.3538.77
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}


def main():
    locale.setlocale(locale.LC_ALL, 'de_DE')

    with open("metadata.json","r") as fp:
        data = json.load(fp)
    
    for i in data:
        print(i)
        name = i['name']
        id_ = i['notation_id']

        dirname = "stocks"

        scrap_date = datetime.date(1990, 1, 1)
        datelist = []
        while(scrap_date <= datetime.date.today()):

            scrap_date_url = ""+str(scrap_date.day)+"." + \
                str(scrap_date.month)+"."+str(scrap_date.year)
            datelist.append(scrap_date_url)
            scrap_date = scrap_date + rd.relativedelta(years=+5)

        data_array = None
        for date_start in datelist:
            URL = ("https://www.onvista.de/onvista/times+sales/popup/historische-kurse/?"
                "notationId="+str(id_)+"&"
                "dateStart="+date_start+"&"
                "interval=Y5&"
                "assetName="+name+"&"
                "exchange=Tradegate"
                )

            response_raw = requests.get(
                URL,
                headers=HEADERS
            )
            soup = bs4.BeautifulSoup(response_raw.content, 'html.parser')

            rows = soup.find_all("tr")
            data = []
            dt = np.dtype([
                ('date', 'object'),
                ('opening', 'f4'),
                ('high', 'f4'),
                ('low', 'f4'),
                ('closing', 'f4'),
                ('volume', 'i4')
            ])

            for r in rows[1:]:
                date = str.strip(r.contents[1].text).split('.')
                date_new_format = date[2]+"-"+date[1]+"-"+date[0]
                opening = locale.atof(str.strip(r.contents[2].text.replace('.', '')))
                high = locale.atof(str.strip(r.contents[3].text.replace('.', '')))
                low = locale.atof(str.strip(r.contents[4].text.replace('.', '')))
                closing = locale.atof(str.strip(r.contents[5].text.replace('.', '')))
                volume = locale.atoi(
                    str.strip(r.contents[6].text.replace('.', '')))

                row = (
                    date_new_format,
                    opening,
                    high,
                    low,
                    closing,
                    volume
                )
                data.append(row)

            if not data:
                continue

            if data_array is None:
                data_array = np.array(data, dtype=dt)
            else:
                data_array = np.concatenate((data_array, np.array(data, dtype=dt)))

        filed = {
            'META': {
                'name': name,
                'id' : id_
            },
            'QUOTES': data_array.tolist()
        }
        filed['META'].update(i)
        try:
            os.mkdir(dirname)
        except OSError:
            pass

        with open(dirname+"/"+name+".json", "w") as fp:
            json.dump(filed, fp)


if __name__ == "__main__":
    main()
