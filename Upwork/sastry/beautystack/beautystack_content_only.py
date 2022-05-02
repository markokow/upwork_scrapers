from dataclasses import dataclass
import re
from tarfile import ExFileObject
import requests
import urllib
import pandas as pd
import csv
import requests_html
from requests_html import HTML
from requests_html import HTMLSession
from typing import List
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
from random import randint
from time import sleep
import io

from tomlkit import key


class BeautyStack_Content:

    def __init__(self, *, max_divisions: int = 3) -> None:
        '''Initialize variables used for scraping.'''
        self.paa_keyword: str = ""
        self.stack_url: str = ""

        self.max_divisions: int = max_divisions

        self.result: List = []

        self.snippets_total: List = []
        self.parsed_snippet: List = []
        self.csv_headers = [None]

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }

    def store_response(self, response, query_name):
        '''Saved response as html.'''
        # if response.status_code == 200:
        print('Saving response as html')
        filename = query_name + ".html"
        with io.open(filename, 'w', encoding = 'utf-8') as html_file:
            html_file.write(response.text)
            print('Done')

    def fetch(self, url):
        '''Fetch the url and returns bs4 object.'''
        response = requests.get(url, headers = self.headers)

        if response.status_code != 200:
            print(f"Status code: {response.status_code}")
            print("Error! Please exit scraper and wait a few hours.")

        return response

    def parse(self, *, html) -> str:
        '''Parse the urls contained in the page and append to results.'''
        content = BeautifulSoup(html, 'lxml')

        features: dict = {}
        
        _data = content.find("div", {"id":"primary"})
        title = content.title.text.strip()
        title = title.replace("\"", "")
        title = title.replace("'", "")

        if _data:

            _content = _data.find("div",{"class":"entry-content"})
            features['url'] = self.url
            features['title'] = title
            features["content"] = _content


        return (features if _data else None)


    def write_csv(self, file_name: str = ''):
        '''Save results to csv.'''
        print('Saving to csv....')

        if self.result: 
            with open(f'{file_name}.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.csv_headers)
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)

        print(f"Saved to {file_name}.csv")

    def sub_beauty(self, url):
        self.url = url
        resp = self.fetch(url = url)
        result = self.parse(html = resp.content)
        
        return (result if result else None)

    def run(self):

        print("Scraper is running...")

        self.now = str(datetime.today()).replace(':','-')

        df = pd.read_csv("beautystack.csv", engine='python')

        final_res: List = []

        counter = 0
        part = 0

        for count, dat in enumerate(df.index):
            # sleep(randint(2,3))
            url = df.iloc[dat,0]
            print(url)

            beauty_res = self.sub_beauty(url = url)
                  
            try:
                output = beauty_res
            except TypeError:
                if count == len(df.index) - 1:
                    df_out = pd.DataFrame(final_res)
                    df_out.to_csv(f"{self.now}_part{part}.csv", index = False)
                    print(f"Saving {self.now}_part{part}.csv")
                    break                    
                else:
                    continue

            counter += 1
            final_res.append(output)

            if count == len(df.index) - 1:
                df_out = pd.DataFrame(final_res)
                df_out.to_csv(f"{self.now}_part{part}.csv", index = False)
                print(f"Saving {self.now}_part{part}.csv")
                break
            
            if (counter % self.max_divisions) == 0:
                part += 1
                df_out = pd.DataFrame(final_res)
                df_out.to_csv(f"{self.now}_part{part}.csv", index = False)
                print(f"Saving {self.now}_part{part}.csv")
                final_res = []
            else:
                continue



if __name__ == '__main__':

    max_divisions: int = 3

    #Run scraper
    scraper = BeautyStack_Content(max_divisions = max_divisions)
    scraper.run()