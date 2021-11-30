import pandas as pd
import requests
import io
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List


class ByJus_Scraper:

    def __init__(self, *,urls: List = []) -> None:
        '''Initialize variables used for scraping.'''
        self.urls: List = urls
        self.url: str = ''

        self.result: List = []

        self.parsed_urls: List = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }

    def fetch(self):
        '''Fetch the url and returns bs4 object.'''
        print(self.url)
        response = requests.get(self.url, headers = self.headers)

        return response

    def parse(self, *, html) -> str:
        '''Parse the urls contained in the page and append to results.'''
        feature: dict = {}
        content = BeautifulSoup(html, 'lxml')

        question = content.find("h1", {"class": "text_contentH1__2_8-o"})
        
        answer = content.find("h2", {"class": "text_contentH1__2_8-o"})
        block = answer.find_all("span", {"class": "mjx-chtml"})

        feature = {
            'question': question.text,
            'answer': ('\n'.join([dat.text for dat in block])).strip(),
        }

        self.result.append(feature)

    def write_excel(self):
        '''Save results to excel.'''
        print('Saving to excel....')

        now = str(datetime.today()).replace(':','-')

        df = pd.DataFrame(self.result)

        df.to_excel(f'{now}.xlsx', encoding='utf-32')

        print(f"Saved to {now}.xlsx")
    
    def store_response(self, *, response, page):
        '''Saved response as html.'''
        if response.status_code == 200:
            print('Saving response as html')
            filename = 'res' + str(page) + '.html'
            with io.open(filename, 'w', encoding = 'utf-8') as html_file:
                html_file.write(response.text)
            print('Done')
        else:
            print('Bad response!')

    def run(self):
        '''Run all cases using the keyword'''
        for url in self.urls:
            self.url = url
            resp = self.fetch()
            self.parse(html = resp.content)

        self.write_excel()

if __name__ == '__main__':

    file =  open('inputs.txt', 'r', encoding='utf-8')
    urls: List = [acc.strip() for acc in file.readlines()]
    #Run scraper
    scraper = ByJus_Scraper(urls= urls)

    scraper.run()
