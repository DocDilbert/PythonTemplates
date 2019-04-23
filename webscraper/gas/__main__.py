import webdb
import re
from bs4 import BeautifulSoup
CONTENT_TYPE="text/html; charset=UTF-8"

def parse_response(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.findAll("div", {"data-tankstelle": True})
    
    ts_id = results[0]["data-tankstelle"]
    headline_tag = results[0].find("h4", {"class" : "headline"})
    headline = headline_tag.string

    address_tag = headline_tag.find_next("p").find_next("p")
    adress = address_tag.text.split("\n")
    adress = adress[2:]
    adress[0] = adress[0].replace("\r","")
    print(ts_id, headline, adress)
    
def main():
    connection = webdb.db.open_db_readonly("webscraper.db")
    cursor = connection.cursor()

    regex = re.compile("/tankstelle/")
    for session, meta in webdb.interface.get_sessions(cursor):
        session_id = meta['session_id']
        requests = webdb.filters.get_requests_where_session_id_and_content_type(cursor, session_id, CONTENT_TYPE)

        requests_filtered = [request for request,_ in requests if regex.match(request.path)]
        
        responses = [
            webdb.filters.get_response_where_session_id_and_request(cursor, session_id, request) 
            for request in requests_filtered
        ]
        for response,_ in responses:
            parse_response(response)

        #

        print("------")

if __name__ == "__main__":
    main()