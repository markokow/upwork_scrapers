import csv
import requests
import io
from bs4 import BeautifulSoup
from typing import List


class PAA_Scraper:

    def __init__(self, *,keyword: str = 'google', max_questions: int = 5) -> None:
        '''Initialize variables used for scraping.'''
        self.keyword: str = keyword
        self.query: str = keyword
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
        content = BeautifulSoup(html, 'lxml')

        answer = content.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd"})[0]
        snippet_block = content.find_all("div", {"class": "xpc"})

        for snippet in snippet_block:
            self.snippets_total.append(snippet.text)

        return answer.text if answer else ""



    def write_csv(self):
        '''Save results to csv.'''
        print('Saving to csv....')

        if self.result: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)

        print("Saved to results.xlsx")
    
    def open_csv(self):

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

        current_total: int  = 0
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


            if self.keyword == self.query:
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

    keyword = 'what is life?'
    max_questions: int = 25

    #Run scraper
    scraper = PAA_Scraper(keyword= keyword, max_questions = max_questions)
    scraper.run()
