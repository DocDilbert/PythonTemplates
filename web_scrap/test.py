import requests
from bs4 import BeautifulSoup

URL = "https://www.heise.de/newsticker/meldung/Missing-Link-Weimar-1919-Meine-Herren-und-Damen-4356582.html"
page = requests.get(URL)

with open("index.html","wb") as file:
    file.write(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')
    for link in soup.find_all('script'):
        print(link)


    with open("index_pretty.html","w") as file2:
        file2.write(soup.prettify())