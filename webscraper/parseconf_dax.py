from bs4 import BeautifulSoup
import re

DATABASE_DIR  = "data_dax/"
DATABASE = "webscraper.db"


class ResponseParser:
    def __init__(self, add_entry):
        self.regex = re.compile(r"-(\d+)-inline\.")
        self.add_entry = add_entry

    def parse_overview(self, session_id, request, response):
        soup = BeautifulSoup(response.content.decode("utf-8"), 'lxml')

        # get index from url
        index =  int(request.get_url().split("?")[1].split("=")[1])
        features_dict = {
            "type" : "einzelkurs_uebersicht",
            "index" : index
        }    

        self.add_entry(session_id, features_dict)

    def parse(self, session_id, request, response):
        url = request.get_url()

        if "kurse_einzelkurs_uebersicht" in url:
            self.parse_overview(session_id, request, response)
        
