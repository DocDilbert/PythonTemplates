import webdb
import re
from bs4 import BeautifulSoup
import time
CONTENT_TYPE="text/html; charset=UTF-8"
def add_entry(session_id, uuid, headline, adress, products ):
    return
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
    
    start = time.time()

    connection = webdb.db.open_db_readonly("webscraper.db")
    cursor = connection.cursor()

    regex = re.compile("/tankstelle/")
    p1 = 0
    p2 = 0
    for session, meta in webdb.interface.get_sessions(cursor):
        session_id = meta['session_id']

        
        print("Parsing session {} / {} --> {}".format(session_id, session.start_datetime, session.end_datetime))
        
        p1_start = time.time()
        requests = webdb.filters.get_requests_where_session_id_and_content_type(cursor, session_id, CONTENT_TYPE)

        requests_filtered = [request for request,_ in requests if regex.match(request.path)]
        
        responses = [
            webdb.filters.get_response_where_session_id_and_request(cursor, session_id, request) 
            for request in requests_filtered
        ]
        p1_end = time.time()

        p1 = p1 + p1_end - p1_start
        p2_start = time.time()
        for response,_ in responses:
            parse_response(session_id, response)

        p2_end = time.time()

        p2 = p2 + p2_end - p2_start

        
    
    end = time.time()
    max_sessions = session_id
    print()
    print("Execution time {:.3f} s.".format(end - start))
    print("Execution time per session {:.3f} s.".format((end - start)/max_sessions))
    print("----")
    print("avg(p1) = {:.3f} s (database access time)".format(p1/max_sessions))
    print("avg(p2) = {:.3f} s (parsing time)".format(p2/max_sessions))

if __name__ == "__main__":
    main()