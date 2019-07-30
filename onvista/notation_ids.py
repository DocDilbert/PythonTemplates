import requests
import bs4
import json

import collections
# chrome 70.0.3538.77
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

def details(url):
    response_raw = requests.get(
        url,
        headers=HEADERS
    )
    soup = bs4.BeautifulSoup(response_raw.content, 'html.parser')

    stammdaten = soup.find('', {'class':'STAMMDATEN'})
    dl_0 = stammdaten.find('dl')
    dd_0 = dl_0.find_all('dd')
    wkn = dd_0[0].text
    isin = dd_0[1].text
    symbol = dd_0[2].text

  
    chart_ex_l = soup.find('', {'id':'chartExchangesLayer'})
    ul_0 = chart_ex_l.find('ul')
    xetra = ul_0.find(text=' Xetra ').parent

    # for further implementations
    _tradegate = ul_0.find(text=' Tradegate ').parent

    xetra_id = xetra['href'].split('=')[1]

    return {
        'notation_id': int(xetra_id),
        'wkn' : wkn,
        'isin' : isin,
        'symbol': symbol
    }


def main():
    ROOT = "https://www.onvista.de"
    URL = ROOT+"/index/einzelwerte/DAX-Index-20735"
    response_raw = requests.get(
        URL,
        headers=HEADERS
    )
    soup = bs4.BeautifulSoup(response_raw.content, 'html.parser')
    wpname = soup.find("span", {"class": "WERTPAPIERNAME"}).find("a")
    index_name = wpname.contents[0].strip()
    tbody = soup.find("tbody", {"class": "table_box_content_zebra"})
    
    entries = tbody.find_all("tr")

    data = []
    for i in entries:
        first = i.find("td")
        ahref = first.find("a")
        name = ahref['title']
        link = ROOT+ahref['href']
        item = collections.OrderedDict({
            'name': name,
            'index' : index_name
        })
        item.update(details(link))
        print(str(item))
        data.append(item)

    with open('metadata.json', 'w') as fP:
        json.dump(
            data,
            fP,
            indent=4
        )


if __name__ == "__main__":
    main()
