import requests
import bs4
import re
import json

# chrome 70.0.3538.77
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

REGEX_NID = re.compile(r"notationId: '(\d*)")


def details(url):
    response_raw = requests.get(
        url,
        headers=HEADERS
    )
    soup = bs4.BeautifulSoup(response_raw.content, 'html.parser')

    m = re.search(REGEX_NID, response_raw.content.decode('utf-8'))

    return {
        'notation_id': int(m[1])
    }


def main():
    ROOT = "https://www.onvista.de"
    URL = ROOT+"/index/einzelwerte/DAX-Index-20735"
    response_raw = requests.get(
        URL,
        headers=HEADERS
    )
    soup = bs4.BeautifulSoup(response_raw.content, 'html.parser')

    tbody = soup.find("tbody", {"class": "table_box_content_zebra"})
    entries = tbody.find_all("tr")

    data = []
    for i in entries:
        first = i.find("td")
        ahref = first.find("a")
        name = ahref['title']
        link = ROOT+ahref['href']
        item = {
            'name': name
        }
        item.update(details(link))
        print(item)
        data.append(item)

    with open('metadata.json', 'w') as fP:
        json.dump(
            data,
            fP,
            indent=4,
            sort_keys=True
        )


if __name__ == "__main__":
    main()
