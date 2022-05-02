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


class CombinedPaa_BeautyStack:

    def __init__(self, *, max_paa: int = 4, max_divisions: int = 3) -> None:
        '''Initialize variables used for scraping.'''
        self.paa_keyword: str = ""
        self.stack_url: str = ""


        self.max_paa: int = max_paa
        self.max_divisions: int = max_divisions

        self.result: List = []

        self.snippets_total: List = []
        self.parsed_snippet: List = []
        self.csv_headers = [None]

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }


    def cleanup(self, string):

        patterns = [
            # r"{2}-{1:0>2}-{0:0>2}",
            # r"{0}-{1:0>2}-{2:0>2}",
            # r"{0}-{1:0>2}",
            r"\d{2}-(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{4}",
            r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d, \d{4}",
            r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2}, \d{4}",
        ]

        for pattern in patterns:
            string = re.sub(pattern, '', string)

        return string

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


    def fetch_query(self, query):

        query = urllib.parse.quote_plus(query)
        response = self.get_source("https://www.google.com/search?q='"+query+"?")

        if response.status_code != 200:
            print(f"Status code: {response.status_code}")
            print("Error! Please exit scraper and wait a few hours.")

        return response

        return response

    def parse_response(self, response: requests_html.HTMLResponse = None):

        # content = BeautifulSoup(response.content, 'lxml', from_encoding="utf-8")
        content = BeautifulSoup(response.content, 'lxml')


        answer = content.find("div", {"class": "V3FYCf"})
        lists: str = ''

        ppl_also_ask = content.find("div", {"jsname": "N760b"})

        if ppl_also_ask:
            all_paas = ppl_also_ask.find_all("div", {"jsname": "Cpkphb"})

            for paa in all_paas:

                data = paa.find("div", {"jsname": "F79BRe"})
                self.snippets_total.append(data["data-q"])

        if answer:
            heading = answer.find("div", {"role":"heading"})
            try:
                lists = "\n".join([val.text.replace("...", "").strip() for val in  answer.find_all("li") if val])
                if lists == None:
                    lists = ""
            except AttributeError:
                lists = ""

            if heading:
                try:
                    texts: List = []

                    for val in heading.find_all("span"):
                        text = val.text.strip()
                        texts.append(text)

                    texts = list(set(texts))
                    texts = "\n".join(texts)

                    answer = texts + lists
                    try:
                        answer = parse(answer, fuzzy_with_tokens=True)[1]
                        answer = ''.join([x for x in answer if x != ' '])
                    except:
                        answer = answer
                    return self.cleanup(answer).strip()
                except AttributeError:
                    try:
                        lists = parse(lists, fuzzy_with_tokens=True)[1]
                        lists = ''.join([x for x in lists if x != ' '])
                    except:
                        lists = lists
                    return self.cleanup(lists).strip()
            else:
                return None
        else:
            return None

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

    def sub_paa(self, keyword: str = ""):
    
            # sleep(randint(2,3))
        self.paa_keyword = keyword
        self.snippets_total = [keyword]
        self.parsed_snippet = []

        question_counter: int = 0

        output_dict: dict = {}
        output_dict['keyword'] = keyword

        while self.snippets_total:

            if question_counter == self.max_paa:
                return output_dict
                # self.result.append(output_dict)
                # break

            for snip in self.snippets_total:
                if snip not in self.parsed_snippet:
                    self.paa_keyword = snip
                    break
                else:
                    continue

            response = self.fetch_query(query = self.paa_keyword)
          #  self.store_response(response=response, query_name=keyword)
            result = self.parse_response(response = response) 


            if result == None:
                if (self.paa_keyword == keyword) &  (len(self.snippets_total) == 1):
                    break
                else:
                    self.parsed_snippet.append(self.paa_keyword)
                    continue
            else:
                self.parsed_snippet.append(self.paa_keyword)
                question_counter+=1
                output_dict['question_' + str(question_counter)] = self.paa_keyword
                output_dict['answer_' + str(question_counter)] = result

                if (self.paa_keyword == keyword) &  (len(self.snippets_total) == 1):
                    return output_dict


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
            keyword = df.iloc[dat,1]
            print(url, " ", keyword)

            beauty_res = self.sub_beauty(url = url)
            

            # stack_res = self.sub_stack(url = url)
            paa_res = self.sub_paa(keyword=keyword)
            
            try:
                output = {**beauty_res, **paa_res}
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

    max_paa: int = 3
    max_divisions: int = 3

    #Run scraper
    scraper = CombinedPaa_BeautyStack(max_paa = max_paa, max_divisions = max_divisions)
    scraper.run()