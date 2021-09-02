import csv
import requests

from typing import List
from bs4 import BeautifulSoup


# import _amazon_selenium
from _amazon_selenium import _classAmazon


class _amazon_scrape():

    def __init__(self, url: str = 'https://www.google.com/search') -> None:
        '''Initialize variables used for scraping.'''

        #base url
        self.base_url: str = url

        #Header
        self._headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}

        #Proxies for UNITED STATES
        # self.http_proxy  = "http://10.10.1.10:3128"
        self.https_proxy = "157.245.222.183:80" #
        # self.ftp_proxy   = "ftp://10.10.1.10:3128"

        self.proxyDict = { 
                    # "http"  : self.http_proxy, 
                    "https" : self.https_proxy, 
                    # "ftp"   : self.ftp_proxy
                    }
        #amazon urls
        self._amazon_url: List[str] = []

        self.result: List = []


    def _fetch(self, _url):
        '''Fetch the url and returns bs4 object.'''
        response = requests.get(_url, self._headers, proxies=self.proxyDict)

        return response



    def _parse(self, _response):
        '''Parse the urls contained in the page and append to results.'''
        content = BeautifulSoup(_response.content, 'lxml')

        _a_links = content.find_all('a')

        for link in _a_links:
            try:
                _url = link['href']
                if 'amazon' in link.text.lower():
                    self._amazon_url.append(_url)
                    # self._innerparse(_url)
            except KeyError:
                continue


    def _write_csv(self,):
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
            
        
    def run(self,):

        #access main url
        main_resp = self._fetch(self.base_url)

        try:
            self._parse(main_resp)
            _data = _classAmazon(self._amazon_url)
            self.result = _data._run()
        except KeyboardInterrupt:
            pass
        # print(self._amazon_url)
        return self.result

        '''Run all cases using the keyword'''


if __name__ == '__main__':


    _test_url = 'https://www.loudersound.com/features/the-best-budget-wireless-headphones'

    #Run scraper
    scraper = _amazon_scrape(_test_url)
    scraper.run()
