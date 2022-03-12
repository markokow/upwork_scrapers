from ast import keyword
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import glob
import csv
import requests
import io
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
from random import randint
from time import sleep
import pandas as pd
import numpy as np
from random import randrange

class PAA_Synonym:
    def __init__(self, *,filepaths: List = [], max_rephrase: int = 1) -> None:
        '''Initialize variables used for scraping.'''
        self.filepaths: List = filepaths
        self.filepath: str = ""
        self.max_rephrase = max_rephrase

        self.base_url: str = 'https://www.thesaurus.com/browse/'
        self.keyword: str = ''
        self.result: str = ''

        self.parsed_idx: List = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }

        self.csv_headers = [None]

    def fetch(self):
        '''Fetch the url and returns bs4 object.'''
        response = requests.get(self.base_url + self.keyword, headers = self.headers)

        return response

    def parse(self, *, html) -> str:
        '''Parse the urls contained in the page and append to results.'''
        content = BeautifulSoup(html, 'lxml')

        block = content.find("div",{"id":"meanings"})

        if block:
            synonyms = block.find_all("li")
        else:
            return False

        if synonyms:
            result = [_.text.strip() for _ in synonyms]
            rndm_idx = randrange(len(result))
            self.result = result[rndm_idx]

            return True

        return False

    def write_csv(self, file_name: str = ''):
        '''Save results to csv.'''
        print('Saving to csv....')

        imgs = [_ for _ in self.csv_headers if "img_src" in _]
        vids = [_ for _ in self.csv_headers if "vid_src" in _]

        new_headers = list(self.csv_headers)[:3] + imgs + vids

        if self.result: 
            with open(f'{file_name}', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = new_headers)
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

    def find_synonym(self, df: pd.DataFrame = pd.DataFrame()):
        df = df.copy()

        ans_columns = [_ for _ in df.columns if "answer" in _]
        keywords = df.keyword.unique()
        df = df.set_index("keyword")

        for key in keywords:
            for ans in ans_columns:
                phrase = df.at[key, ans]

                if phrase is not np.nan:
                    print(f"Phrase: {phrase}")
                    listed = phrase.split()
                    # print(listed)
                    while True:
                        rndm_idx = randrange(len(listed))

                        if rndm_idx in self.parsed_idx:
                            continue

                        self.parsed_idx.append(rndm_idx)

                        if len(self.parsed_idx) == len(listed):
                            print("No available synonyms from thesaurus.com. Nothing was replaced.")
                            break

                        # print(rndm_idx)
                        self.keyword = listed[rndm_idx]
                        # print(self.keyword)
                        resp = self.fetch()
                        # print(resp.status_code)
                        if resp.status_code == 200:
                            # self.store_response(response=resp, page = 200)
                            _bool = self.parse(html = resp.content)

                            if _bool:
                                df.at[key,ans] = df.at[key,ans].replace(self.keyword, self.result)
                                print(f"Replaced \"{self.keyword}\" with \"{self.result}\"")
                                print("\n")
                                break
                        
                    self.parsed_idx = []
                    
        return df
    
    def run(self):
        '''Run all cases using the paths.'''
        output_folder_path = os.path.join(os.getcwd(), 'Output')

        if not(os.path.exists(output_folder_path)):
            os.makedirs(output_folder_path)

        for _ in self.filepaths:
            print(_)
            try:
                df = pd.read_csv(_)
                df = self.find_synonym(df = df)
            except:
                pass
            finally:
                filename = _.replace(".csv","")
                df.to_csv(os.path.join('Output',f"{filename}_replaced_synonyms.csv"))
                print(f"File saved to Output/{filename}_replaced_synonyms.csv")
    
        print("All csvs replaced.")

if __name__ == '__main__':
    '''Run main file.'''
    extension = 'csv'
    data = glob.glob('*.{}'.format(extension))

    filepaths: List = [_.strip() for _ in data]
    max_rephrase: int = 3
    
    # Run scraper
    scraper = PAA_Synonym(filepaths= filepaths, max_rephrase = max_rephrase)
    scraper.run()