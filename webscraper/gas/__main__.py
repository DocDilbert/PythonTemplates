import webdb
import re
from bs4 import BeautifulSoup
CONTENT_TYPE="text/html; charset=UTF-8"
def add_entry(session_id, uuid, headline, adress, products ):
    print(uuid, headline, adress)

    for zahl, product,wann1, wann2 in products:
        print("\t{:9} {:20}{:25}{}".format(zahl, product,wann1,wann2))

def parse_response(session_id, response, add_entry=add_entry):
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.findAll("div", {"data-tankstelle": True})
    
    uuid = results[0]["data-tankstelle"]
    headline_tag = results[0].find("h4", {"class" : "headline"})
    headline = headline_tag.string

    address_tag = headline_tag.find_next("p").find_next("p")

    #Extract adress
    adress = address_tag.text.split("\n")
    adress = adress[2:]
    adress[0] = adress[0].replace("\r","")
   
    products = []
    div_with_class_preis = soup.find_all("div", {"class","preis"})
    for preisc in div_with_class_preis:

        span_with_class_zahl = preisc.find("span", {"class","zahl"}).text
        product = preisc.find("strong").text
        span_with_title=preisc.find("span", {"title":True})
        wann1 = str.strip(str(span_with_title.next_sibling))
        wann2 = span_with_title['title']
        
        products.append([
            span_with_class_zahl, 
            product,
            wann1,
            wann2
        ])
        
    add_entry(session_id, uuid, headline, adress, products)


    
def main():
    connection = webdb.db.open_db_readonly("webscraper.db")
    cursor = connection.cursor()

    regex = re.compile("/tankstelle/")
    for _, meta in webdb.interface.get_sessions(cursor):
        session_id = meta['session_id']
        requests = webdb.filters.get_requests_where_session_id_and_content_type(cursor, session_id, CONTENT_TYPE)

        requests_filtered = [request for request,_ in requests if regex.match(request.path)]
        
        responses = [
            webdb.filters.get_response_where_session_id_and_request(cursor, session_id, request) 
            for request in requests_filtered
        ]
        for response,_ in responses:
            parse_response(session_id, response)

        #

        print("------")

if __name__ == "__main__":
    main()