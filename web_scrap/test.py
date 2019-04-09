import requests
from bs4 import BeautifulSoup

URL = "https://www.heise.de/newsticker/"

#chrome 70.0.3538.77
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
page = requests.get(URL, headers=headers)

with open("index.html","wb") as file:
    file.write(page.content)
    soup = BeautifulSoup(page.content, 'html.parser')
    for link in soup.find_all('script'):
        print(link)


    with open("index_pretty.html","w") as file2:
        file2.write(soup.prettify())