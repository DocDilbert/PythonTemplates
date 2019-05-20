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
        header1_div = soup.find("div", {"class":"einzelkurs_header"})
        header = header1_div.find("h1").text
        header2_div = header1_div.find_next("div", {"class":"einzelkurs_header"})
        isin_wkn_span = header2_div.find("span",{"class": "leftfloat bottom_aligned"})
        isin_wkn = [x.strip().split(" ")[1] for x in isin_wkn_span.text.split("|")]

        table = header2_div.find_next("table")
        gattung_td = table.find_next("td", {"headers":"gattung"})
 
        # get index from url
        index =  int(request.get_url().split("?")[1].split("=")[1])
        features_dict = {
            "type" : "uebersicht",
            "index" : index,
            "header" : header,
            "isin" : isin_wkn[0],
            "wkn" : isin_wkn[1],
            "gattung" : gattung_td.text
        }  
        if "Index" in gattung_td.text:
            land_td = table.find("td", {"headers":"land"})
            features_dict.update( {
                "land" : land_td.text
            })

        elif "Aktie" in gattung_td.text:
            branche_td = gattung_td.find_next("td", {"headers":"gattung"})
            marktkapitalisierung_td =  branche_td.find_next("td", {"headers":"gattung"})

            boersen_platz = table.find("td", {"headers":"boerse"})
            boersen_td = boersen_platz.find_next("td", {"headers":"boerse"})
            indizes = [x.text for x in boersen_td.find_all("option")]
    
            features_dict.update( {
                "branche" : branche_td.text,
                "marktkapitalisierung" : marktkapitalisierung_td.text,
                "boersen_platz" : boersen_platz.text,
                "indizes" : indizes
            })

        self.add_entry(session_id, features_dict)

    def parse(self, session_id, request, response):
        url = request.get_url()

        if ("einzelkurs_uebersicht" in url) and ("offset" not in url):
            self.parse_overview(session_id, request, response)

        
