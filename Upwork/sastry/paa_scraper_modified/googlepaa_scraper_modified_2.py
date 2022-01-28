from ast import Index
import csv
import requests
import io
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
import time

class PAA_Scraper:

    def __init__(self, *,keywords: List = [], max_questions: int = 5, max_divisions: int  = 5) -> None:
        '''Initialize variables used for scraping.'''
        self.keywords: List = keywords
        self.keyword: str = ""
        self.query: str = ""
        self.max_questions: int = max_questions
        self.max_divisions: int = max_divisions

        self.base_url: str = 'https://www.google.com/search'
        self.result: List = []

        self.snippets_total: List = [self.keyword]
        self.parsed_snippet: List = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }

    def fetch(self):
        '''Fetch the url and returns bs4 object.'''
        # response = requests.get(f"https://www.google.com/search?q='+{self.keyword}", headers = self.headers)
        response = requests.get(f"http://api.scraperapi.com?api_key=89f53273207f9aacdce3069e17dfceb0&url=https://www.google.com/search?q='+{self.keyword}", headers = self.headers)

        return response

    def parse(self, *, html) -> str:
        '''Parse the urls contained in the page and append to results.'''
        print(self.keyword)

        content = BeautifulSoup(html, 'lxml')

        answer = content.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd"})[0]
        snippet_block = content.find_all("div", {"class": "xpc"})

        heading = answer.find("div", {"class":"Ey4n2"})

        try:
            lists = "\n".join([val.text for val in  answer.find("ul", {"class":"yRG22b v7pIac"}).find_all("div", {"class":"BNeawe s3v9rd AP7Wnd"}) if val])
            if lists == None:
                lists = ""
        except AttributeError:
            lists = ""

        for snippet in snippet_block:
            question = snippet.text if snippet else ""

            if question.endswith('?'):
                self.snippets_total.append(question)

        heading = heading.text if heading else ""

        _answer = heading + "\n" + lists

        if heading.strip() == "" or lists.strip() == "":
            _answer = answer.text

        _answer = _answer.replace("\"", "")
        _answer = _answer.replace("'", "")  
        _answer = _answer.strip()

        return _answer

    def write_csv(self, filename: str):
        '''Save results to csv.'''
        print('Saving to csv....')

        if self.result: 
            with open(f'{filename}.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)

        print(f"Saved to {filename}.csv")
    
    def open_csv(self):
        '''Opens a csv.'''
        print("opening csv")
        with open('results.csv', 'r', newline = '', encoding= 'utf-8') as csv_file:
            _dict_reader = csv.DictReader(csv_file)
            self._taken = list(_dict_reader)
        

        self._done = [_val['valid_urls'] for _val in self._taken]

        self.result = self._taken

        print(self.result)


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
        now = str(datetime.today()).replace(':','-')

        part: int = 1
        legit_counter: int = 1
        for count, keyword in enumerate(self.keywords):

            current_total: int  = 0
            tries_counter: int = 0
            current_question: str = ''
            last_question: str = ''

            self.query = keyword
            self.keyword = keyword
            self.snippets_total = [keyword]
            self.parsed_snippet = []

            output_dict: dict = {}
            output_dict['keyword'] = self.query
            

            while True:
                for snip in self.snippets_total:
                    if snip not in self.parsed_snippet:
                        self.keyword = snip
                        break
                    else:
                        continue

                current_question = self.keyword

                if tries_counter == 3:
                    self.parsed_snippet.append(self.keyword)
                    continue
                        
                resp = self.fetch()
                self.store_response(response=resp, page = 0)

                if resp.status_code == 429:
                    time.sleep(3)
                    continue

                try:
                    ans = self.parse(html  = resp.content)
                except IndexError:
                    self.parsed_snippet.append(self.keyword)
                    continue

                self.parsed_snippet.append(self.keyword)

                if len(ans) < 150:
                    self.parsed_snippet.append(self.keyword)
                    continue

                if current_question == last_question:
                    # self.store_response(response=resp, page = 0)
                    tries_counter += 1
                    continue
                else:
                    current_total += 1
                    output_dict['question_' + str(current_total)] = self.keyword
                    output_dict['answer_' + str(current_total)] = ans
                    last_question = current_question

                if current_total == self.max_questions:
                    break

                self.result.append(output_dict)

            
            legit_counter += 1
            if (legit_counter+1) % self.max_divisions == 0:
                self.write_csv(filename=f"{now}_part{part}")
                self.result = []
                part += 1
            elif (count == len(keyword)-1):
                self.write_csv(filename=f"{now}_part{part}")
     


if __name__ == '__main__':

    keywords: List = []
    with open('keywords.csv', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        keywords = list(reader)

    keywords =  [acc[0].strip() for acc in keywords]

    max_questions: int = 3
    max_divisions: int = 2

    #Run scraper
    scraper = PAA_Scraper(keywords= keywords, max_questions = max_questions, max_divisions = max_divisions)
    scraper.run()