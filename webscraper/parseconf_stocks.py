from bs4 import BeautifulSoup
import re
from datetime import datetime


class Config:
    DATABASE_DIR = "data_stocks/"
    DATABASE = "webscraper.db"

    RAW_DATA_DIR = "data_stocks/"
    RAW_DATA_FILE = "stocks_raw.json"


class ResponseParser:
    def __init__(self, add_entry):
        self.regex = re.compile(r"-(\d+)-inline\.")
        self.add_entry = add_entry
        self.title_regex = re.compile(
            r".*in (\w*)\s(.*)\. Das Geschäftsjahr endet am (.*)"
        )

    def detect_currency(self, str):
        if "€" in str:
            return ("euro", "€")
        elif "$" in str:
            return ("dollar", "$")
        else:
            return ("unbekannt", "?")

    def convert_to_float(self, trailing, pstr):
        pstr = pstr.replace(trailing, "")
        pstr = pstr.strip()
        pstr = pstr.replace(".", "")
        pstr = pstr.replace(",", ".")
        pstr = pstr.replace(u'\xa0', u' ')
        pstr = pstr.replace(u'\xb1', u'')  # +-

        try:
            val = float(pstr)
        except ValueError:
            val = None
        return val

    def convert_markt_kapitalisierung(self, mstr):
        if " Mio." in mstr:
            mstr = int(mstr.replace(" Mio.", "000000"))
        elif " Mrd." in mstr:
            mstr = int(mstr.replace(" Mrd.", "000000000"))
        elif " Bio." in mstr:
            mstr = int(mstr.replace(" Bio.", "000000000"))
        elif "--" in mstr:
            mstr = None
        else:
            raise Exception(mstr)

        return mstr

    def parse_history(self, session_id, request, response):
        soup = BeautifulSoup(response.content.decode("utf-8"), 'lxml')

        header1_div = soup.find("div", {"class": "einzelkurs_header"})
        header2_div = header1_div.find_next(
            "div", {"class": "einzelkurs_header"})
        sample_time_span = header2_div.find(
            "span", {"class": "rightfloat bottom_aligned"})
        isin_wkn_span = header2_div.find(
            "span", {"class": "leftfloat bottom_aligned"})
        isin_wkn = [x.strip().split(" ")[1]
                    for x in isin_wkn_span.text.split("|")]

        aktueller_wert = header2_div.find("span", {"title": "aktueller Wert"})

        currency = self.detect_currency(aktueller_wert.text)
        kurshistorie = soup.find("div", {"class": "kurshistorie"})

        rows = kurshistorie.find_all("tr")

        historie = []
        for row in rows[1:]:
            cell = row.find_all("td")
            date = cell[0]
            eroeffnung = cell[1]
            hoch = cell[2]
            tief = cell[3]
            schlusskurs = cell[4]
            historie.append(
                {
                    "datum": date.text,
                    "eroeffnung": self.convert_to_float(currency[1], eroeffnung.text),
                    "hoch": self.convert_to_float(currency[1], hoch.text),
                    "tief": self.convert_to_float(currency[1], tief.text),
                    "schlusskurs": self.convert_to_float(currency[1], schlusskurs.text)
                }
            )

        # get index from url
        index = int(request.get_url().split("?")[1].split("=")[1])

        # "17.05.2019  17:45"
        st = datetime.strptime(sample_time_span.text.replace(
            u'\xa0', u' '), '%d.%m.%Y  %H:%M')

        features_dict = {
            "name": header1_div.find("h1").text,
            "type": "historie",
            "url": request.get_url(),
            "abtastzeit": st.isoformat(),
            "waehrung": currency[0],
            "index": index,
            "historie": historie,
            "isin": isin_wkn[0],
            "wkn": isin_wkn[1]
        }

        self.add_entry(session_id, features_dict)

    def parse_overview(self, session_id, request, response):
        soup = BeautifulSoup(response.content.decode("utf-8"), 'lxml')
        header1_div = soup.find("div", {"class": "einzelkurs_header"})
        header2_div = header1_div.find_next(
            "div", {"class": "einzelkurs_header"})
        isin_wkn_span = header2_div.find(
            "span", {"class": "leftfloat bottom_aligned"})
        isin_wkn = [x.strip().split(" ")[1]
                    for x in isin_wkn_span.text.split("|")]

        sample_time_span = header2_div.find(
            "span", {"class": "rightfloat bottom_aligned"})
        table = header2_div.find_next("table")
        aktueller_kurs = table.find("td", {"headers": "aktueller_kurs"})
        tageshoch = table.find("td", {"headers": "tageshoch"})
        tagestief = table.find("td", {"headers": "tagestief"})
        eroeffnung = table.find("td", {"headers": "eroeffnung"})
        vortag = table.find("td", {"headers": "vortag"})
        wochenhoch = table.find("td", {"headers": "wochenhoch"})
        wochentief = table.find("td", {"headers": "wochentief"})
        gattung_td = table.find_next("td", {"headers": "gattung"})

        vwd_info_box = gattung_td.find_all_next(
            "div", {"class", "vwd_infobox"})

        vwd_info_box_left = vwd_info_box[0]
        vwd_info_box_mid = vwd_info_box[1]
        vwd_info_box_right = vwd_info_box[2]

        eine_woche = vwd_info_box_left.find("td", {"headers": "eine_woche"})
        ein_monat = vwd_info_box_mid.find("td", {"headers": "ein_monat"})
        drei_monate = vwd_info_box_right.find("td", {"headers": "drei_monate"})
        sechs_monate = vwd_info_box_left.find(
            "td", {"headers": "sechs_monate"})
        ein_jahr = vwd_info_box_mid.find("td", {"headers": "ein_jahr"})
        drei_jahre = vwd_info_box_right.find("td", {"headers": "drei_jahre"})
        fuenf_jahre = vwd_info_box_left.find("td", {"headers": "fuenf_jahre"})

        teaser = gattung_td.find_next("div", {"class": "teaserhp"})
        headline = None
        news = []
        if teaser:
            ahref = teaser.find("a").get("href")

            headline = teaser.find("h4", {"class": "headline"}).text
            date = teaser.find("p", {"class": "subheadline"}).text
            news.append((date, headline, ahref))
            newstables = teaser.find_all_next("span", {"class": "newstable"})
            for entry in newstables:
                spans = entry.find_all("span")
                date = spans[0].text.replace("|", "").strip()
                headline = spans[1].text.strip()
                ahref = spans[0].parent.get("href")
                news.append((date, headline, ahref))

        # get index from url
        index = int(request.get_url().split("?")[1].split("=")[1])

        currency = self.detect_currency(aktueller_kurs.text)
        # "17.05.2019  17:45"
        st = datetime.strptime(sample_time_span.text.replace(
            u'\xa0', u' '), '%d.%m.%Y  %H:%M')

        features_dict = {
            "url": request.get_url(),
            "type": "uebersicht",
            "news": news,
            "kurse": {
                "aktueller_kurs": self.convert_to_float(currency[1], aktueller_kurs.text),
                "tageshoch": self.convert_to_float(currency[1], tageshoch.text),
                "tagestief": self.convert_to_float(currency[1], tagestief.text),
                "eroeffnung": self.convert_to_float(currency[1], eroeffnung.text),
                "vortag": self.convert_to_float(currency[1], vortag.text),
                # 52 Wochen
                "wochenhoch": self.convert_to_float(currency[1], wochenhoch.text),
                # 52 Wochen
                "wochentief": self.convert_to_float(currency[1], wochentief.text),
            },
            "waehrung": currency[0],
            "index": index,
            "name": header1_div.find("h1").text,
            "isin": isin_wkn[0],
            "wkn": isin_wkn[1],
            "gattung": gattung_td.text,
            "abtastzeit": st.isoformat(),
            "performance": {
                "eine_woche": self.convert_to_float("%", eine_woche.text),
                "ein_monat": self.convert_to_float("%", ein_monat.text),
                "drei_monate": self.convert_to_float("%", drei_monate.text),
                "sechs_monate": self.convert_to_float("%", sechs_monate.text),
                "ein_jahr": self.convert_to_float("%", ein_jahr.text),
                "drei_jahre": self.convert_to_float("%", drei_jahre.text),
                "fuenf_jahre": self.convert_to_float("%", fuenf_jahre.text)
            }
        }
        if "Index" in gattung_td.text:
            land_td = table.find("td", {"headers": "land"})
            features_dict.update({
                "land": land_td.text
            })

        elif "Aktie" in gattung_td.text:
            branche_td = gattung_td.find_next("td", {"headers": "gattung"})
            marktkapitalisierung_td = branche_td.find_next(
                "td", {"headers": "gattung"})

            boersen_platz = table.find("td", {"headers": "boerse"})
            boersen_td = boersen_platz.find_next("td", {"headers": "boerse"})
            indizes = [x.text for x in boersen_td.find_all("option")]

            features_dict.update({

                "branche": branche_td.text,
                "marktkapitalisierung": self.convert_markt_kapitalisierung(marktkapitalisierung_td.text),
                "boersen_platz": boersen_platz.text,
                "indizes": [x.replace(u"\xae", "").strip() for x in indizes]
            })

        self.add_entry(session_id, features_dict)

    def parse_table(self, soup, title):

        bilanz_hl = soup.find(text=title)
        bilanz = bilanz_hl.find_next("table")
        title_hl = bilanz_hl.parent.next_sibling.next_sibling
        if (title_hl.name == "span") or (title_hl.name == "h2"):
            title = title_hl.text
        else:
            title = ""
        header = [x.text for x in bilanz.find_all("th")]

        data = [
            [
                y.text
                for y in x.find_all("td")
            ]
            for x in bilanz.find_all("tr")
        ]

        re = {
            'title': title,
            'header': header,
            'data': data
        }
        match = self.title_regex.match(title)
        if match:

            re.update(
                {
                    'quantifier': match[1],
                    'currency': match[2],
                    'fiscal_year_end': match[3]
                }
            )

        return re

    def parse_profil(self, session_id, request, response):
        soup = BeautifulSoup(response.content.decode("utf-8"), 'lxml')
        header1_div = soup.find("div", {"class": "einzelkurs_header"})
        header2_div = header1_div.find_next(
            "div", {"class": "einzelkurs_header"})
        isin_wkn_span = header2_div.find(
            "span", {"class": "leftfloat bottom_aligned"})
        isin_wkn = [x.strip().split(" ")[1]
                    for x in isin_wkn_span.text.split("|")]
        sample_time_span = header2_div.find(
            "span", {"class": "rightfloat bottom_aligned"})

        # "17.05.2019  17:45"
        st = datetime.strptime(sample_time_span.text.replace(
            u'\xa0', u' '), '%d.%m.%Y  %H:%M')

        features_dict = {
            "url": request.get_url(),
            "type": "profil",
            "isin": isin_wkn[0],
            "wkn": isin_wkn[1],
            "abtastzeit": st.isoformat(),
            "bilanz": self.parse_table(soup, 'Bilanz'),
            "guv": self.parse_table(soup, 'GuV'),
            "cashflow": self.parse_table(soup, 'Cashflow'),
            "wertpapierdaten": self.parse_table(soup, 'Wertpapierdaten'),
            "bewertungszahlen": self.parse_table(soup, 'Bewertungszahlen'),
            "mitarbeiter": self.parse_table(soup, 'Mitarbeiter'),
            "aktionaerstruktur": self.parse_table(soup, 'Aktionärsstruktur:'),

        }
        self.add_entry(session_id, features_dict)

    def parse(self, session_id, request, response):
        url = request.get_url()

        if ("kurse_einzelkurs_uebersicht" in url) and ("offset" not in url):
            pass
            self.parse_overview(session_id, request, response)
        elif ("kurse_einzelkurs_history" in url):
            pass
            self.parse_history(session_id, request, response)
        elif ("kurse_einzelkurs_profil" in url):
            self.parse_profil(session_id, request, response)
