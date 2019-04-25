import webdb
import re
from bs4 import BeautifulSoup
import time
from lxml import etree

CONTENT_TYPE="text/html; charset=UTF-8"

class FileWriter:
    def __init__(self):
        self.f = open("out.csv", "w")

    def add_entry(self, session_id, uuid, headline, adress, products ):
        

        
        for zahl, product,wann1, wann2 in products:
            self.f.write('{};"{}";"{}";"{}";"{}";"{}";"{}";"{}"\n'.format(
                session_id,
                uuid, 
                headline, 
                " / ".join(adress),
                zahl, 
                product,
                wann1,
                wann2
            ))

def parse_response(session_id, response, add_entry):
    p3 = time.time()
    soup = BeautifulSoup(response.content.decode("utf-8") ,'lxml')
    p3 = time.time() - p3

    p4 =  time.time()
    div_with_data = soup.find("div", {"data-tankstelle": True})
    uuid = div_with_data["data-tankstelle"]

    headline_tag = div_with_data.find("h4", {"class" : "headline"})
    headline = headline_tag.string

    address_tag = headline_tag.find_next("p").find_next("p")

    #Extract adress
    adress = address_tag.text.split("\n")
    adress = adress[2:]
    adress[0] = adress[0].replace("\r","")
   
    products = []
    div_with_class_preis = address_tag.find_all_next("div", {"class","preis"})
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
    p4 = time.time() - p4
    return p3, p4

    
def main():
    
    start = time.time()

    connection = webdb.db.open_db_readonly("webscraper.db")
    cursor = connection.cursor()

    regex = re.compile("/tankstelle/")
    p1 = 0
    p2 = 0
    p2_0 = 0
    p2_1 = 0

    file_writer = FileWriter()
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
            p2_0_, p2_1_ = parse_response(session_id, response, add_entry=file_writer.add_entry)
            p2_0 = p2_0 + p2_0_
            p2_1 = p2_1 + p2_1_

        p2_end = time.time()

        p2 = p2 + p2_end - p2_start

        
    
    end = time.time()
    max_sessions = session_id
    print()
    print("Execution time {:.3f} s.".format(end - start))
    print("Execution time per session {:.3f} s.".format((end - start)/max_sessions))
    print("----")
    print("  avg(p1) = {:.3f} s (database access time)".format(p1/max_sessions))
    print("  avg(p2) = {:.3f} s (parsing time)".format(p2/max_sessions))
    print("----")
    print("avg(p2_0) = {:.3f} s (creation time)".format(p2_0/max_sessions))
    print("avg(p2_1) = {:.3f} s (searching time)".format(p2_1/max_sessions))
    print("----")

if __name__ == "__main__":
    main()