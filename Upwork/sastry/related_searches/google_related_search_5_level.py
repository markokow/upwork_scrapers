import csv
import requests
import io
import pandas as pd
from bs4 import BeautifulSoup
from typing import List
import random

class Google_Related_Search:
    def __init__(self, *,keywords: List = [], max_levels: int = 3) -> None:
        '''Initialize variables used for scraping.'''
        self.keywords: List = keywords
        self.keyword: str = ""
        self.query: str = ""
        self.max_levels = max_levels

        self.base_url: str = 'https://www.google.com/search'
        self.result: List = []

        self.snippets_total: List = [self.keyword]
        self.parsed_snippet: List = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }

    def fetch(self):
        '''Fetch the url and returns bs4 object.'''
        response = requests.get(f"https://www.google.com/search?q='+{self.keyword}", headers = self.headers)

        return response

    def parse(self, *, html) -> str:
        '''Parse the urls contained in the page and append to results.'''
        # print(self.keyword)
        content = BeautifulSoup(html, 'lxml')

        all_divs = content.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd lRVwie"})

        data = [x.text.strip() for x in all_divs if x]
        return data

    def fetch_n_parse(self, *, data: List):
        '''Recursion for fetch and parse.'''
        print(data, len(data))
        if len(data) <= self.max_levels-1:
            self.keyword = data[-1]
            resp = self.fetch()
            relateds = self.parse(html = resp.content)

            for related in relateds:
                temp = data + [related]
                self.fetch_n_parse(data = temp)
        else:
            self.result.append(data)

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
    
    def result_to_excel(self,headers: List = [], data: List = []):
        'Converted data to styled excel.'
        parsed_list: List = []

        parsed_unique: List = []
        multi_match: dict = {}
        multi_match_color: dict = {}
        done_color: List = []

        final_data: List = []

        for dat in data:
            interem_data: List = []
            for idx, dat_2 in enumerate(dat):
                if idx < self.max_levels - 1:
                    if dat[:idx+1] in parsed_list:
                        interem_data.append("")
                    else:
                        parsed_list.append(dat[:idx+1])    
                        interem_data.append(dat_2)
                else:
                    interem_data .append(dat_2)
            
            final_data.append(interem_data)

        for idx_1, dat_1 in enumerate(final_data):
            for idx_2, dat_2 in enumerate(dat_1):
                if dat_2 in parsed_unique and dat_2 != '':
                    try:
                        multi_match[dat_2] += 1
                    except KeyError:
                        multi_match[dat_2] = 2
                    
                    if dat_2 not in multi_match_color.keys():
                        
                        while True:
                            color = "#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
                            if color in done_color:
                                continue
                            else:
                                done_color.append(color)
                                break
                        multi_match_color[dat_2] = color
                else:
                    parsed_unique.append(dat_2)

        df = pd.DataFrame(final_data, columns=headers)
 
        df = df.style.applymap(lambda x: ("background-color: " + multi_match_color[x]) if x in multi_match.keys() else '')
        df.to_excel(f'{self.query}.xlsx', engine = 'openpyxl', index=False)

    def run(self):
        '''Run all cases using the keyword'''   
        headers: List = []
        
        for x in range(self.max_levels):
            headers.append('level'+str(x))

        for keyword in self.keywords:
            self.result = []
            data: List = []
            self.query = keyword
            data.append(keyword)
            self.fetch_n_parse(data = data)
            self.result_to_excel(headers = headers, data = self.result)


if __name__ == '__main__':

    file =  open('keywords.txt', 'r', encoding='utf-8')
    keywords: List = [acc.strip() for acc in file.readlines()]
    max_levels: int = 5

    #Run scraper
    scraper = Google_Related_Search(keywords= keywords, max_levels = max_levels)
    scraper.run()
