from bs4 import BeautifulSoup
import re

DATABASE_DIR  = "data_dax/"
DATABASE = "webscraper.db"

RAW_DATA_DIR = "data_dax/"
RAW_DATA_FILE = "boerse_raw.json"

class ResponseParser:
    def __init__(self, add_entry):
        self.regex = re.compile(r"-(\d+)-inline\.")
        self.add_entry = add_entry

    def parse_overview(self, session_id, request, response):
        soup = BeautifulSoup(response.content.decode("utf-8"), 'lxml')
        header1_div = soup.find("div", {"class":"einzelkurs_header"})
        header2_div = header1_div.find_next("div", {"class":"einzelkurs_header"})
        isin_wkn_span = header2_div.find("span",{"class": "leftfloat bottom_aligned"})
        isin_wkn = [x.strip().split(" ")[1] for x in isin_wkn_span.text.split("|")]

        sample_time_span = header2_div.find("span",{"class": "rightfloat bottom_aligned"})
        table = header2_div.find_next("table")
        aktueller_kurs = table.find("td", {"headers":"aktueller_kurs"})
        tageshoch = table.find("td", {"headers":"tageshoch"})
        tagestief = table.find("td", {"headers":"tagestief"})
        eroeffnung = table.find("td", {"headers":"eroeffnung"})
        vortag = table.find("td", {"headers":"vortag"})
        wochenhoch = table.find("td", {"headers":"wochenhoch"})
        wochentief = table.find("td", {"headers":"wochentief"})
        gattung_td = table.find_next("td", {"headers":"gattung"})
        
        vwd_info_box = gattung_td.find_all_next("div", {"class","vwd_infobox"})
        
        vwd_info_box_left  = vwd_info_box[0]
        vwd_info_box_mid   = vwd_info_box[1]
        vwd_info_box_right = vwd_info_box[2]

        eine_woche = vwd_info_box_left.find("td",{"headers":"eine_woche"})
        ein_monat = vwd_info_box_mid.find("td",{"headers":"ein_monat"})
        drei_monate = vwd_info_box_right.find("td",{"headers":"drei_monate"})
        sechs_monate = vwd_info_box_left.find("td",{"headers":"sechs_monate"})
        ein_jahr = vwd_info_box_mid.find("td",{"headers":"ein_jahr"})
        drei_jahre = vwd_info_box_right.find("td",{"headers":"drei_jahre"})
        fuenf_jahre = vwd_info_box_left.find("td",{"headers":"fuenf_jahre"})
        # get index from url
        index =  int(request.get_url().split("?")[1].split("=")[1])

        features_dict = {
            "type" : "uebersicht",
            "kurse" : {
                "aktueller_kurs" : aktueller_kurs.text.replace(u'\xa0', u' '),
                "tageshoch" : tageshoch.text.replace(u'\xa0', u' '),
                "tagestief" : tagestief.text.replace(u'\xa0', u' '),
                "eroeffnung" : eroeffnung.text.replace(u'\xa0', u' '),
                "vortag" : vortag.text.replace(u'\xa0', u' '),
                "wochenhoch": wochenhoch.text.replace(u'\xa0', u' '), # 52 Wochen
                "wochentief": wochentief.text.replace(u'\xa0', u' '), # 52 Wochen
            },
            "index" : index,
            "name" : header1_div.find("h1").text,
            "isin" : isin_wkn[0],
            "wkn" : isin_wkn[1],
            "gattung" : gattung_td.text,
            "abtastzeit" : sample_time_span.text.replace(u'\xa0', u' '),
            "performance" : {
                "eine_woche" : eine_woche.text,
                "ein_monat" : ein_monat.text,
                "drei_monate" : drei_monate.text,
                "sechs_monate" : sechs_monate.text,
                "ein_jahr" : ein_jahr.text,
                "drei_jahre" : drei_jahre.text,
                "fuenf_jahre": fuenf_jahre.text
            }
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

        
