from bs4 import BeautifulSoup
import re


class ResponseParser:
    def __init__(self, add_entry):
        self.regex = re.compile(r"-(\d+)-inline\.")
        self.add_entry = add_entry

    def parse(self, session_id, request, response):
        soup = BeautifulSoup(response.content.decode("utf-8"), 'lxml')

        results = soup.find_all("div", {"class":"job-element-row"})
        
        for result in results:
            title_tag = result.find(class_='job-element__url-title-text')
            title = title_tag.text.strip("\n")
            
            company_tag = result.find(class_='job-element__body__company')
            company = company_tag.text.strip("\n")

            location_tag = result.find(class_='job-element__body__location')
            location = location_tag.text.strip("\n")

            date_tag = result.find(class_='job-element__date')
            datetime_tag = date_tag.find('time')

            details_tag= result.find(class_='job-element__body__details')
            details = details_tag.text.strip("\n")

            
            url_tag= result.find(class_="job-element__url")
            uuid_search = self.regex.search(url_tag['href'])

            features_dict = {
                'title': title,
                'company': company,
                'location': location,
                'datetime': datetime_tag['datetime'],
                'details' : details,
                'uuid' : uuid_search.group(1)
            }
            
            self.add_entry(session_id, features_dict)
