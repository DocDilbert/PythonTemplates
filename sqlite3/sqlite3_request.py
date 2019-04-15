import requests
import logging
import zlib
import time
from bs4 import BeautifulSoup
from sqlliteblob import insert_blob, extract_blob, create_or_open_db

URL = "https://www.heise.de/newsticker/"

#chrome 70.0.3538.77
HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

def main():
    FORMAT = "[%(levelname)-6s] %(filename)14s:%(lineno)3s / %(funcName)s - %(message)s"

    logging.basicConfig(
        format=FORMAT, 
        level=logging.INFO)

    #for i in range(0,100):
    #print("Request {}".format(i))
    page = requests.get(URL, headers=HEADERS)
    #print(page.content)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    for link in soup.find_all('a'):
        print(link.get('href'))
        #print(type(page.content))

    
        # conn = create_or_open_db("newsticker.db")
        # cursor = conn.cursor()
        # insert_blob(cursor, URL, zlib.compress(page.content))
        # conn.commit()
        # time.sleep(6)
    

if __name__ == "__main__":
    main()