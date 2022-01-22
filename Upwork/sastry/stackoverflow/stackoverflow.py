import csv
import requests
import io
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime

class StackOverFlow:
    def __init__(self, *,urls: List = [], max_answers: int = 3) -> None:
        '''Initialize variables used for scraping.'''
        self.urls: List = urls
        self.url: str = ""
        self.max_answers = max_answers

        self.base_url: str = 'https://www.google.com/search'
        self.result: List = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }

        self.csv_headers = [None]

    def fetch(self):
        '''Fetch the url and returns bs4 object.'''
        response = requests.get(self.url, headers = self.headers)

        return response

    def parse(self, *, html) -> str:
        '''Parse the urls contained in the page and append to results.'''
        content = BeautifulSoup(html, 'lxml')

        features: dict = {}
        title = content.title.text.strip().replace(' - Stack Overflow', " ").strip()
        title = title.replace("\"", "")
        title = title.replace("'", "")
        all_answers = content.select('div[class*="answer js-answer"]')

        if all_answers:
            features['url'] = self.url
            features['title'] = title

            count = 1
            for ans in all_answers:
                answer = ans.find("div", {"class": "answercell post-layout--right"})
                post_body = answer.find("div", {"class": "s-prose js-post-body"})
                post_body = str(post_body)
                post_body = post_body.replace("<div class=\"s-prose js-post-body\" itemprop=\"text\">", " ")
                post_body = post_body[:-6]
                post_body = post_body.strip()
                post_body = post_body.replace("\"", "")
                post_body = post_body.replace("'", "")
                post_body = post_body.strip()
    
                features[f'best_answer_{count}'] = post_body

                if count == self.max_answers:
                    break
                else:
                    count+=1
            
            if len(features.keys()) > len(self.csv_headers):
                self.csv_headers = features.keys()

            self.result.append(features)

    def write_csv(self):
        '''Save results to csv.'''
        print('Saving to csv....')

        now = str(datetime.today()).replace(':','-')

        if self.result: 
            with open(f'{now}.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.csv_headers)
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)

        print(f"Saved to {now}.csv")

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
        '''Run all cases using the urls'''
        print("Scraping is running please don't exit...")
        for url in self.urls:
            self.url = url
            resp = self.fetch()
            self.parse(html = resp.content)

            # print(self.result)

        self.write_csv()

if __name__ == '__main__':
    '''Run main file.'''
    file =  open('stack_urls.txt', 'r', encoding='utf-8')
    urls: List = [acc.strip() for acc in file.readlines()]
    max_answers: int = 3
    
    #Run scraper
    scraper = StackOverFlow(urls= urls, max_answers = max_answers)
    scraper.run()
