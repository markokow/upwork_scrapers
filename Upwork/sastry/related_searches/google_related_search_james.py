from base64 import encode
import csv
import requests
import io
from bs4 import BeautifulSoup
from typing import List
from requests_html import HTMLSession
import urllib
import pandas as pd
import time

class Google_Related_Search:
    def __init__(self, *,keywords: List = [], max_searches: int = 3) -> None:
        '''Initialize variables used for scraping.'''
        self.keywords: List = keywords
        self.keyword: str = ""
        self.query: str = ""
        self.max_searches = max_searches

        self.base_url: str = 'https://www.google.com/search'
        self.result: List = []

        self.related_searches: List = []
        self.parsed_keyword: List = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }

    def get_source(self, url):
        """Return the source code for the provided URL. 

        Args: 
            url (string): URL of the page to scrape.

        Returns:
            response (object): HTTP response object from requests_html. 
        """
        try:
            session = HTMLSession()
            response = session.get(url)
            return response

        except requests.exceptions.RequestException as e:
            print(e)

    def fetch_query(self, query):

        query = urllib.parse.quote_plus(query)
        response = self.get_source("https://www.google.com/search?q=+"+query)

        print(response.status_code)

        return response

    def fetch(self):
        '''Fetch the url and returns bs4 object.'''
        # response = requests.get(f"https://www.google.com/search?q='+{self.keyword}", headers = self.headers)
        response = requests.get(f"https://www.google.co.uk/search?q=+{self.keyword}", headers = self.headers)
        
        

        return response

    def parse(self, *, html) -> str:
        '''Parse the urls contained in the page and append to results.'''
        # print(self.keyword)
        content = BeautifulSoup(html, 'lxml')
        # all_divs = content.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd lRVwie"})
        all_divs = content.find_all("div", {"class": "s75CSd OhScic AB4Wff"})

        if all_divs:
            for div in all_divs:
                data = div.text.strip()
                if data in self.related_searches:
                    continue
                else:
                    print(data)
                    self.related_searches.append(data)

    def open_csv(self):
        '''Opens a csv.'''
        print("opening csv")
        with open('results.csv', 'r', newline = '', encoding= 'utf-8') as csv_file:
            _dict_reader = csv.DictReader(csv_file)
            self._taken = list(_dict_reader)
        

        self._done = [_val['valid_urls'] for _val in self._taken]

        self.result = self._taken

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

        time_1 = time.time()

        df = pd.read_csv("Products for Keywords - Rex.csv", encoding='utf-8')
        df = df.set_index(["No"])
        new_df = df[df['Keyword 1'].isnull()]
    
        cols = [x for x in new_df.columns if x.__contains__("Keyword")]

        try:
            added_counter = 0
            for dat in df.index:   
                if not pd.isna(df.loc[dat,cols[0]]):
                    continue
                else:
                    added_counter += 1
                    keyword = df.loc[dat,"Product Title"].encode('cp850', errors='replace').decode('cp850')
                # for idx, keyword in enumerate(keywords):
                    self.result = []
                    self.related_searches = [keyword]
                    self.parsed_keyword = []
                    break_outer: bool = False

                    previous_keyword: str = ""
                    while True:
                        counter += 1
                        for query in self.related_searches:
                            if query in self.parsed_keyword:
                                if (query == previous_keyword) and (len(self.related_searches) == 1):
                                    print("aoks")
                                    break_outer = True
                                    break
                                else:
                                    continue
                            else:
                                self.keyword = query
                                self.parsed_keyword.append(query)
                                break

                        if break_outer:
                            break

                        print("umabot dito")


                        response = self.fetch_query(query=self.keyword)
                        # self.store_response(response=response, page = 10)
                        self.parse(html = response.content)

                        previous_keyword = self.keyword

                        print("umabhot dito 2")
                        
                        if len(self.related_searches) > self.max_searches:
                            self.related_searches = self.related_searches[1:self.max_searches]
                            break
                        else:
                            continue

                    for count, value in enumerate(self.related_searches):
                        print(dat, cols[count])
                        print(value)
                        df.loc[dat, cols[count]] = str(value)
        except Exception as e:
            print(e)
        finally:
            keywords_left = new_df['Product Title'].apply(lambda x: x.encode('cp850', errors='replace').decode('cp850')).values.tolist()

            time_2 = time.time()
            print("Total time spent: ", time_2 - time_1)
            print(f"{added_counter} keywords added")
            print(f"{len(keywords_left)} keywords left")
            df.to_csv("Products for Keywords - Rex.csv", encoding = "utf-8")
            print("Saved to csv")


if __name__ == '__main__':

    file =  open('keywords.txt', 'r', encoding='utf-8')
    keywords: List = [acc.strip() for acc in file.readlines()]
    max_searches: int = 31
    
    #Run scraper
    scraper = Google_Related_Search(keywords= keywords, max_searches = max_searches)
    scraper.run()
