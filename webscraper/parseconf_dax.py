from bs4 import BeautifulSoup
import re

DATABASE_DIR  = "data_dax/"
DATABASE = "webscraper.db"


class ResponseParser:
    def __init__(self, add_entry):
        self.regex = re.compile(r"-(\d+)-inline\.")
        self.add_entry = add_entry

    def parse(self, session_id, request, response):
        soup = BeautifulSoup(response.content.decode("utf-8"), 'lxml')

        features_dict = {
            "url" : request.get_url()
        }    
        self.add_entry(session_id, features_dict)
