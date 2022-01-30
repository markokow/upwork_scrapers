from multiprocessing.sharedctypes import Value
import re
import requests
import urllib
import pandas as pd
import io 
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


from tomlkit import key

class ModifiedPaaScraper:

    def __init__(self, *,keywords: List = [], max_questions: int = 5, max_division: int = 50) -> None:
        '''Initialize variables used for scraping.'''
        self.keywords: List = keywords
        self.keyword: str = ""
        self.query: str = ""
        self.max_questions: int = max_questions
        self.max_division: int = max_division

        self.result: List = []

        self.snippets_total: List = []
        self.parsed_snippet: List = []
        self.csv_headers = [None]

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

    def fetch_query(self, query):

        query = urllib.parse.quote_plus(query)
        response = self.get_source("https://www.google.com/search?q="+query+"?")

        return response

    def parse_response(self, response: requests_html.HTMLResponse = None):

        content = BeautifulSoup(response.content, 'lxml', from_encoding="utf-8")

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
                    except ValueError:
                        answer = answer
                    return self.cleanup(answer).strip()
                except AttributeError:
                    try:
                        lists = parse(lists, fuzzy_with_tokens=True)[1]
                        lists = ''.join([x for x in lists if x != ' '])
                    except ValueError:
                        lists = lists
                    return self.cleanup(lists).strip()
            else:
                return None
        else:
            return None

    def store_response(self, response, query_name):
        '''Saved response as html.'''
        # if response.status_code == 200:
        print('Saving response as html')
        filename = query_name + ".html"
        with io.open(filename, 'w', encoding = 'utf-8') as html_file:
            html_file.write(response.text)
            print('Done')

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

    def run(self):

        _parsed_counter: int = 0
        _part: int = 0

        self.now = str(datetime.today()).replace(':','-')
        
        for count, keyword in enumerate(self.keywords):
           # sleep(randint(2,3))
            print(keyword)
            self.query = keyword
            self.keyword = keyword
            self.snippets_total = [keyword]
            self.parsed_snippet = []

            question_counter: int = 0

            output_dict: dict = {}
            output_dict['keyword'] = self.query

            while self.snippets_total:

                if question_counter == self.max_questions:
                    self.result.append(output_dict)
                    break

                for snip in self.snippets_total:
                    if snip not in self.parsed_snippet:
                        self.keyword = snip
                        break
                    else:
                        continue

                response = self.fetch_query(query = self.keyword)
                result = self.parse_response(response = response) 

                if result == None:
                    if (self.keyword == keyword) &  (len(self.snippets_total) == 1):
                        break
                    else:
                        self.parsed_snippet.append(self.keyword)
                        continue
                else:
                    self.parsed_snippet.append(self.keyword)
                    question_counter+=1
                    output_dict['question_' + str(question_counter)] = self.keyword
                    output_dict['answer_' + str(question_counter)] = result


                    if (self.keyword == keyword) &  (len(self.snippets_total) == 1):
                        self.result.append(output_dict)
                        break

            if len(output_dict.keys()) == 1:
                continue
            else:
                _parsed_counter += 1

                if len(output_dict.keys()) > len(self.csv_headers):
                    self.csv_headers = output_dict.keys()
        
                if count == len(self.keywords)-1:
                    _part += 1
                    self.write_csv(file_name=f"{self.now}_part{_part}")
                    break

                if _parsed_counter % self.max_division == 0:
                    _part += 1
                    self.write_csv(file_name=f"{self.now}_part{_part}")
                    self.csv_headers = [None]
                    self.result = []


if __name__ == '__main__':

    keywords: List = []
    with open('keywords.csv', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        keywords = list(reader)

    keywords =  [acc[0].strip() for acc in keywords]

    max_questions: int = 10
    max_divisions: int = 3

    #Run scraper
    scraper = ModifiedPaaScraper(keywords= keywords, max_questions = max_questions, max_division = max_divisions)
    scraper.run()