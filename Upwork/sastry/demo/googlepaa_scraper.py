import csv
import requests
import io
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime


class PAA_Scraper:

    def __init__(self, *,keywords: List = [], max_questions: int = 5) -> None:
        '''Initialize variables used for scraping.'''
        self.keywords: List = keywords
        self.keyword: str = ""
        self.query: str = ""
        self.max_questions: int = max_questions

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

        return _answer

    def write_csv(self):
        '''Save results to csv.'''
        print('Saving to csv....')

        now = str(datetime.today()).replace(':','-')

        if self.result: 
            with open(f'{now}.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)

        print(f"Saved to {now}.xlsx")
    
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
        for keyword in self.keywords:

            current_total: int  = 0

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
                        
                resp = self.fetch()
                ans = self.parse(html  = resp.content)
                self.parsed_snippet.append(self.keyword)

                if len(ans) < 150:
                    continue

                if self.keyword == self.query:
                    #self.store_response(response=resp, page = 0)
                    continue
                else:
                    current_total += 1
                    output_dict['question_' + str(current_total)] = self.keyword
                    output_dict['answer_' + str(current_total)] = ans

                if current_total == self.max_questions:
                    break

            self.result.append(output_dict)

        self.write_csv()

if __name__ == '__main__':

    file =  open('keywords.txt', 'r', encoding='utf-8')
    keywords: List = [acc.strip() for acc in file.readlines()]
    max_questions: int = 25

    #Run scraper
    scraper = PAA_Scraper(keywords= keywords, max_questions = max_questions)
    scraper.run()
