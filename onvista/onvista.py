
import requests
import bs4
from bs4 import BeautifulSoup

import dateutil.relativedelta as rd
import numpy as np
import datetime 
import locale

locale.setlocale(locale.LC_ALL, 'de_DE')

# chrome 70.0.3538.77
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

Name = "Daimler"


scrap_date = datetime.date(1990,1,1)
datelist=[]
while(scrap_date<=datetime.date.today()):
    
    scrap_date_url = ""+str(scrap_date.day)+"."+str(scrap_date.month)+"."+str(scrap_date.year)
    datelist.append(scrap_date_url)
    scrap_date = scrap_date + rd.relativedelta(years=+5)


data_array = None
for date_start in datelist:
    URL = ("https://www.onvista.de/onvista/times+sales/popup/historische-kurse/?"
        "notationId=28859632&"
        "dateStart="+date_start+"&"
        "interval=Y5&"
        "assetName="+Name+"&"
        "exchange=Tradegate"
    )

    response_raw = requests.get(
        URL,
        headers=HEADERS
    )
    soup = BeautifulSoup(response_raw.content, 'html.parser')
    table = soup.find("table")
    rows = soup.find_all("tr")
    data = []
    for r in rows[1:]:
        date = str.strip(r.contents[1].text).split('.')
        date_new_format = date[2]+"-"+date[1]+"-"+date[0]
        opening = locale.atof(str.strip(r.contents[2].text))
        high = locale.atof(str.strip(r.contents[3].text))
        low = locale.atof(str.strip(r.contents[4].text))
        closing = locale.atof(str.strip(r.contents[5].text))
        volume = locale.atoi(str.strip(r.contents[6].text.replace('.','')))
        row = [
            date_new_format,
            opening,
            high,
            low,
            closing,
            volume
        ]
        data.append(row)
    
    if len(data)==0:
        continue

    if data_array is None:
        data_array = np.array(data)
    else:
        data_array = np.concatenate((data_array, np.array(data) ))

with open("daimler.csv", "w") as fp:
    for r in data_array:
        fp.write("{}, {}, {}, {}, {}, {}\n".format(
            r[0], r[1], r[2], r[3], r[4], r[5])
        )


