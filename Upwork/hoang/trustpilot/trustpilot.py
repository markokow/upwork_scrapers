import csv
from unittest import result
from urllib.error import ContentTooShortError
import requests
import io
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
from random import randint
from time import sleep
import urllib.parse

class TrustPilot:
    def __init__(self, *,urls: List = [], max_divisions: int = 3) -> None:
        '''Initialize variables used for scraping.'''
        self.urls: List = urls
        self.url: str = ""
        self.max_divisions = max_divisions

        self.base_url: str = 'https://www.google.com/search'
        self.result: List = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }

        self.csv_headers = [None]

    def fetch(self):
        '''Fetch the url and returns bs4 object.'''
        response = requests.get(self.url, headers = self.headers)

        return response

    def parse(self, *, html) -> str:
        '''Parse the urls contained in the page and append to results.'''
        content = BeautifulSoup(html, 'lxml')

        papers = content.find_all("div", {"class":"paper_paper__29o4A"})
        _next = content.find("a", {"name": "pagination-button-next"})


        if papers:
            for paper in papers:

                _features: dict = {}
                # print(paper.text)

                _name = paper.find("p", {"class": "typography_typography__23IQz typography_h4__IhMYK typography_weight-heavy__36UHe typography_fontstyle-normal__1_HQI styles_displayName__1LIcI"}).text
                _logo = paper.find("div",{"class":"styles_content__3mwYr"}).find("img").get("src")
                try:
                    _trust_score = paper.find("div",{"class":"styles_rating__2FRLX"}).find("span", {"class":"styles_desktop__3N0-b"}).text
                except:
                    _trust_score = ''

                # print(_trust_score.text)

                _features["name"] = _name
                _features["logo_link"] = _logo
                _features["trust_score"] = _trust_score 

                self.result.append(_features)

        if _next:
            _relative = _next.get("href")
            _abs = urllib.parse.urljoin(self.url, _relative)

            print(_abs)

            self.url = _abs

            resp = self.fetch()
            self.parse(html = resp.content)

        # # print(self.result)

        # for res in self.result:
        #     print(res)


        

        # for paper in papers:
        #     print(paper.text)


    def write_csv(self, file_name: str = ''):
        '''Save results to csv.'''
        print('Saving to csv....')

        # imgs = [_ for _ in self.csv_headers if "img_src" in _]
        # vids = [_ for _ in self.csv_headers if "vid_src" in _]

        # new_headers = list(self.csv_headers)[:3] + imgs + vids

        if self.result: 
            with open(f'{file_name}', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)

        print(f"Saved to {file_name}")

    def store_response(self, *,response, page):
        '''Saved response as html.'''
        if response.status_code == 200:
            print('Saving response as html')
            filename = 'res' + str(page) + '.html'
            with io.open(filename, 'w', encoding = 'utf-8') as html_file:
                html_file.write(response.text)
            print('Done')
        else:
            print('Bad response!')
  
    def load_response(self):   
        '''Load an html file.'''
        html = ''
        with open('res.html', 'r') as html_file:
            for line in html_file.read():
                html += line
        return html
    
    def run(self):
        '''Run all cases using the urls'''
        self.now = str(datetime.today()).replace(':','-')
        # self.url = "https://fr-be.trustpilot.com/categories/online_marketplace?numberofreviews=0&status=all&timeperiod=0"
        self.url = "https://www.trustpilot.com/categories/online_marketplace?numberofreviews=0&status=all&timeperiod=0"
        resp = self.fetch()

        self.parse(html = resp.content)
        self.write_csv(file_name=f"{self.now}.csv")




if __name__ == '__main__':
    '''Run main file.'''
    #Run scraper
    scraper = TrustPilot()
    scraper.run()
