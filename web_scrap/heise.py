import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

URL = "https://www.heise.de/newsticker/archiv/2006/01"
#URL = "https://www.spiegel.de/schlagzeilen/index-siebentage.html"
#chrome 70.0.3538.77
HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


def load_css(css_link, cookies, no):
    o = urlparse(URL)
    page_link = o.scheme+"://"+o.netloc+css_link['href']
    o2 = urlparse(page_link)
    print(o2)
    print("PAGE_LINK: "+page_link)
    with open("test{}.css".format(no),"wb") as file:
        css = requests.get(page_link, headers=HEADERS, cookies=cookies)
        file.write(css.content)
    
    css_link['href'] = "test{}.css".format(no)

def main():
    page = requests.get(URL, headers=HEADERS)

    with open("index.html","wb") as file:
        print(page.headers)
        file.write(page.content)
        soup = BeautifulSoup(page.content, 'html.parser')
        no=0
        jar = page.cookies
        print(jar)
        for link in soup.find_all('link', {"type" : "text/css"}):
            load_css(link, jar, no)
            no+=1


        with open("index_pretty.html","w") as file2:
            file2.write(soup.prettify())

if __name__ == "__main__":
    main()