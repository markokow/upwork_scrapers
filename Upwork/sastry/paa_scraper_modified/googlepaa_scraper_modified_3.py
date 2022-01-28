import csv
import requests
import io
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
from urllib.parse import urlencode


class PAA_Scraper:

    def __init__(self, *,keywords: List = [], max_questions: int = 5, max_division: int = 50) -> None:
        '''Initialize variables used for scraping.'''
        self.keywords: List = keywords
        self.keyword: str = ""
        self.query: str = ""
        self.max_questions: int = max_questions
        self.max_division: int = max_division

        self.base_url: str = 'https://www.google.com/search'
        self.result: List = []

        self.snippets_total: List = [self.keyword]
        self.parsed_snippet: List = []

        self.now: str = ''
        self.API = '89f53273207f9aacdce3069e17dfceb0'

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }

    def get_url(self,url):
        # payload = {'api_key': self.API, 'url': url, 'country_code': 'in'}
        payload = {'api_key': self.API, 'url': url}
        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)

        return proxy_url

    def fetch(self):
        '''Fetch the url and returns bs4 object.'''
        # response = requests.get(f"http://api.scraperapi.com?api_key=89f53273207f9aacdce3069e17dfceb0&url=https://www.google.com/search?q='+{self.keyword}", headers = self.headers)
        # response = requests.get(f"https://www.google.com/search?q='+{self.keyword}", headers = self.headers)
        url = self.get_url(url = f"https://www.google.com/search?q=+'{self.keyword}")
        response = requests.get(url, headers = self.headers)

        return response

    # def parse(self, *, html) -> str:
    #     '''Parse the urls contained in the page and append to results.'''
    #     print(self.keyword)

    #     content = BeautifulSoup(html, 'lxml')

    #     answer = content.find_all("div", {"class": "yp1CPe wDYxhc NFQFxe viOShc LKPcQc"})[0]
    #     # answer = content.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd"})[0]
    #     snippet_block = content.find_all("div", {"jsname": "Cpkphb"})

    #     # heading = answer.find("div", {"class":"Ey4n2"})
    #     heading = answer.find("div", {"role":"heading"})
    #     print("answer")
    #     print(answer)
    #     print("heading")
    #     print(heading)
    #     print("snippet")
    #     print(snippet_block)


    #     try:
    #         # lists = "\n".join([val.text for val in  answer.find("ul", {"class":"yRG22b v7pIac"}).find_all("div", {"class":"BNeawe s3v9rd AP7Wnd"}) if val])
    #         lists = "\n".join([val.text for val in  answer.find_all("li", {"class":"TrT0Xe"}) if val])
    #         if lists == None:
    #             lists = ""
    #     except AttributeError:
    #         lists = ""

    #     if snippet_block:
    #         for snippet in snippet_block:
    #             question = snippet.text if snippet else ""

    #             if question.endswith('?'):
    #                 self.snippets_total.append(question)
    #     else:
    #         return None

    #     heading = heading.text if heading else ""

    #     _answer = heading + "\n" + lists

    #     if heading.strip() == "" or lists.strip() == "":
    #         _answer = answer.text

    #     _answer = _answer.replace("\"", "")
    #     _answer = _answer.replace("'", "")  
    #     _answer = _answer.strip()

    #     return _answer

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
        
        print(_answer)
        print(heading)
        print(snippet_block)

        return _answer

    def write_csv(self, file_name: str = ''):
        '''Save results to csv.'''
        print('Saving to csv....')

        if self.result: 
            with open(f'{file_name}.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)

        print(f"Saved to {file_name}.csv")
    
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
        counter = 1
        part: int = 1
        self.now = str(datetime.today()).replace(':','-')
        actual_counter = 0
        attempts: int = 0

        for keyword in self.keywords:
            actual_counter+=1
            attempts = 0

            print("working on: ", keyword)
            current_total: int  = 0

            self.query = keyword
            self.keyword = keyword
            self.snippets_total = [keyword]
            self.parsed_snippet = []

            output_dict: dict = {}
            output_dict['keyword'] = self.query

            # try:
            while True:
                if attempts == 3:
                    break

                for snip in self.snippets_total:
                    if snip not in self.parsed_snippet:
                        self.keyword = snip
                        break
                    else:
                        continue

                print("current question: ", self.keyword)

                resp = self.fetch()
                self.store_response(response=resp, page = 0)

                if resp.status_code != 200:
                    attempts += 1
                    print(resp.status_code)

                    if attempts == 3:
                        attempts = 0
                        break
                    continue
                try:
                    ans = self.parse(html  = resp.content)
                except (IndexError, TypeError):
                    continue

                self.parsed_snippet.append(self.keyword)

                if len(ans) < 150 or self.keyword == self.query:
                    self.parsed_snippet.append(self.keyword)
                    continue
                
                else:
                    current_total += 1
                    output_dict['question_' + str(current_total)] = self.keyword
                    output_dict['answer_' + str(current_total)] = ans
            
                print(output_dict)

                if current_total == self.max_questions:
                    break

            if output_dict:
                self.result.append(output_dict)
            else:
                continue

            print(self.result)

            if actual_counter == len(self.keywords):
                self.write_csv(file_name=f"{self.now}_part{part}.csv")
                break

            if counter % self.max_division == 0:
                self.write_csv(file_name=f"{self.now}_part{part}.csv")
                self.result = []
                self.snippets_total = []
                self.parsed_snippet = []
                part+=1
            
            else:
                if ((len(self.keywords) - counter) > self.max_division):
                    counter+=1
                    continue
                else:
                    self.write_csv(file_name=f"{self.now}_part{part}.csv")
                    part+=1

            counter+=1

if __name__ == '__main__':

    keywords: List = []
    with open('keywords.csv', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        keywords = list(reader)

    keywords =  [acc[0].strip() for acc in keywords]

    max_questions: int = 3
    max_divisions: int = 3

    #Run scraper
    scraper = PAA_Scraper(keywords= keywords, max_questions = max_questions, max_division = max_divisions)
    scraper.run()