import csv
import requests
import io

from typing import List
from bs4 import BeautifulSoup

class SimilarWebScrape():


    def __init__(self):

        self.base_url = 'https://majestic.com/'

        self.user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

        #overall result
        self.result: List[dict] = []

    def _fetch(self,url):

        response = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'})

        return response

    def _parse(self,response):

        result_dict = {}

        print('parsing', response.url)

        _content = BeautifulSoup(response.content, 'lxml')

        result_dict['URL'] = response.url

        ranks = _content.find_all('div', class_ = 'websiteRanks-valueContainer js-websiteRanksValue')

        print(ranks)

        # print(content)

    
    def _run(self):


        response = self._fetch(self.base_url)

        print(response)

        self._store_response(response)

        self._parse(response)

    def _store_response(self, response):
        if response.status_code == 200:
            print('Saving response as html')
            filename = 'res.html'
            with io.open(filename, 'w', encoding = 'utf-8') as html_file:
                html_file.write(response.text)
            print('Done')
        else:
            print('Bad response!')

    def write_csv(self,):
        '''Save results to csv.'''
        print('Saving to csv....')

        if self.result: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)
            print("Saved to results.xlsx")
        
        else:
            print('No data was saved')




if __name__ == '__main__':

    scrape = SimilarWebScrape()
    scrape._run()

    # scrape._run()