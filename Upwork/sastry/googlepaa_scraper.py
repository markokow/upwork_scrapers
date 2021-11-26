import csv
import requests
from bs4 import BeautifulSoup
import io
from datetime import datetime
from urllib.request import urlopen, Request
from typing import Any, Union, List


class GoogleScraper:

    def __init__(self, *,keyword: str = 'google') -> None:
        '''Initialize variables used for scraping.'''
        self.keyword: str = keyword
        self.pages: int = pages
        self.base_url: str = 'https://www.google.com/search'
        self.keyword_list: List = []
        self.result: List = []
        self._taken: List = []
        self._done: List = []
        self._counter: int = 0

        self.pagination_params = {
            'q':'query',
            'oq':'none',
            'gs_lcp':'Cgdnd3Mtd2l6EAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAELADEEMyCgguEMgDELADEEMyCgguEMgDELADEEMyCgguEMgDELADEEMyCgguEMgDELADEENKBQg4EgExSgQIQRgAUABYAGCNog5oAXACeACAAZ8FiAGfBZIBAzUtMZgBAMgBDcABAQ',
            'sclient':'gws-wiz',
            'start': '0',
            'uact':'5',
        }

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Alt-Used': 'www.google.com',
            'Connection': 'keep-alive',

            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers',
        }

    def fetch(self, *,page):
        '''Fetch the url and returns bs4 object.'''
        self.pagination_params['q'] = self.keyword
        self.pagination_params['oq'] = self.keyword

        response = requests.get(self.base_url, params = self.pagination_params, headers = self.headers)

        return response

    def parse(self, *,html):
        '''Parse the urls contained in the page and append to results.'''
        content = BeautifulSoup(html, 'lxml')


    def write_csv(self):
        '''Save results to csv.'''
        print('Saving to csv....')

        if self.result: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)

        print("Saved to results.xlsx")
    
    def open_csv(self):

        print("opening csv")
        with open('results.csv', 'r', newline = '', encoding= 'utf-8') as csv_file:
            _dict_reader = csv.DictReader(csv_file)
            self._taken = list(_dict_reader)
        

        self._done = [_val['valid_urls'] for _val in self._taken]

        self.result = self._taken

        print(self.result)


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
        '''Run all cases using the keyword'''

        # #Run all pages
        resp = self.fetch(0)
        self.parse(resp.content)
        self.store_response(resp,0)


if __name__ == '__main__':

    keyword = 'what is the real purpose of life'
    #Run scraper
    scraper = GoogleScraper(keyword= keyword)
    scraper.run()
