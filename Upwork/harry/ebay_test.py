import csv
from regex import F
import requests
import io
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
import pandas as pd

class Ebay:
    def __init__(self,) -> None:
        '''Initialize variables used for scraping.'''
        self.url: str = ""
        self.base_url: str = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=blood+pressure+cuff&_sacat=0'
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
        # print(content)

        items = content.find_all("li", {"class":"s-item s-item__pl-on-bottom"})
        
        for item in items:

            title = item.find("h3", {"class":"s-item__title"}).text.strip()
            price = item.find("span", {"class":"s-item__price"}).text.strip()
            rating   = item.find("span", {"class":"s-item__etrs-text"})
            rating = rating.text.strip() if rating else 'None'

            self.result.append(
                {'title': title,
                'price': price,
                'rating': rating}
            )

    def write_csv(self):
        '''Save results to csv.'''
        print('Saving to csv....')

        now = str(datetime.now()).replace(':', '-')

        if self.result: 
            with open(f'{now}.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.csv_headers)
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)

        print(f"Saved to {now}.csv")


    def store_response(self, *,response, page):
        '''Saved response as html.'''
        if response.status_code == 200:
            print('Saving response as html')
            filename = f'res{str(page)}.html'
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
        print("Scraping is running please don't exit...")
        self.url = self.base_url
        res = self.fetch()
        # self.store_response(response=res, page=1)
        self.parse(html=res.content)
        # self.write_csv()
        df = pd.DataFrame(self.result)
        df.to_csv('result.csv', index=True)

if __name__ == '__main__':
    '''Run main file.'''
    
    #Run scraper
    scraper = Ebay()
    scraper.run()
