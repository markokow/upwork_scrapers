import csv
import requests
import io
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime

class Brainly:
    def __init__(self, *,urls: List = [], max_answers: int = 3) -> None:
        '''Initialize variables used for scraping.'''

        # self.base_url: str = 'https://brainly.com/graphql/us?operationName=feed&variables={"gradeIds":[],"subjectIds":[5],"statusId":"ALL","cursor":"Y3Vyc29yOjE2NTY1Njg2MTU=","feedType":"PUBLIC","first":20}&extensions={"persistedQuery":{"version":1,"sha256Hash":"a18dcee8ff57280c79a46e830df335650f7c74a60266dceb332a055b8a315b16'
        # self.base_url: str = "/graphql/us?operationName=feed&variables=%7B%22gradeIds%22%3A%5B%5D%2C%22subjectIds%22%3A%5B5%5D%2C%22statusId%22%3A%22ALL%22%2C%22cursor%22%3A%22Y3Vyc29yOjE2NTY1Njg2MTU%3D%22%2C%22feedType%22%3A%22PUBLIC%22%2C%22first%22%3A20%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22a18dcee8ff57280c79a46e830df335650f7c74a60266dceb332a055b8a315b16%22%7D%7D HTTP/2"
        self.base_url: str = "https://brainly.com/graphql/us?operationName=feed&variables=%7B\"gradeIds\"%3A[]%2C\"subjectIds\"%3A[5]%2C\"statusId\"%3A%22ALL\"%2C\"cursor\"%3A%22Y3Vyc29yOjE2NTY1Njg2MTU%3D\"%2C\"feedType\"%3A%22PUBLIC\"%2C\"first\"%3A20%7D&extensions=%7B%22persistedQuery\"%3A%7B%22version\"%3A1%2C\"sha256Hash\"%3A\"a18dcee8ff57280c79a46e830df335650f7c74a60266dceb332a055b8a315b16\"%7D%7D"
        self.result: List = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'host': 'brainly.com',
            # User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://brainly.com/subject/history',
            'content-type': 'application/json',
            'Connection': 'keep-alive',
            'Cookie': 'https://brainly.com/graphql/us?operationName=feed&variables=%7B%22gradeIds%22%3A%5B%5D%2C%22subjectIds%22%3A%5B5%5D%2C%22statusId%22%3A%22ALL%22%2C%22cursor%22%3Anull%2C%22feedType%22%3A%22PUBLIC%22%2C%22first%22%3A20%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22a18dcee8ff57280c79a46e830df335650f7c74a60266dceb332a055b8a315b16%22%7D%7D',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0.2'
        }

        self.csv_headers = [None]

    def fetch(self):
        '''Fetch the url and returns bs4 object.'''
        response = requests.get(self.base_url, headers = self.headers)

        return response

    def parse(self, *, html) -> str:
        '''Parse the urls contained in the page and append to results.'''
        content = BeautifulSoup(html, 'lxml')

    # def write_csv(self):
    #     '''Save results to csv.'''
    #     print('Saving to csv....')

    #     now = str(datetime.today()).replace(':','-')

    #     if self.result: 
    #         with open(f'{now}.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
    #             writer_object = csv.DictWriter(csv_file, fieldnames = self.csv_headers)
    #             writer_object.writeheader()

    #             for row in self.result:
    #                 writer_object.writerow(row)

    #     print(f"Saved to {now}.csv")

    # def open_csv(self):
    #     '''Opens a csv.'''
    #     print("opening csv")
    #     with open('results.csv', 'r', newline = '', encoding= 'utf-8') as csv_file:
    #         _dict_reader = csv.DictReader(csv_file)
    #         self._taken = list(_dict_reader)
        

    #     self._done = [_val['valid_urls'] for _val in self._taken]

    #     self.result = self._taken

    def store_response(self, *,response):
        '''Saved response as html.'''
        if response.status_code != 200:
            print('Saving response as html')
            # filename = 'res' + str(page) + '.html'
            with io.open("html.html", 'w', encoding = 'utf-8') as html_file:
                html_file.write(response.text)
            print('Done')
        else:
            print('Bad response!')
  
    # def load_response(self):   
    #     '''Load an html file.'''
    #     html = ''
    #     with open('res.html', 'r') as html_file:
    #         for line in html_file.read():
    #             html += line
    #     return html
    
    def run(self):
        '''Run all cases using the urls'''
        # print("Scraping is running please don't exit...")
        data = self.fetch()
        self.store_response(response = data)

        print(data)
        # for url in self.urls:
        #     self.url = url
        #     resp = self.fetch()
        #     self.parse(html = resp.content)

        #     # print(self.result)

        # self.write_csv()

if __name__ == '__main__':
    '''Run main file.'''
    # file =  open('stack_urls.txt', 'r', encoding='utf-8')
    max_answers: int = 3
    
    #Run scraper
    scraper = Brainly(max_answers = max_answers)
    scraper.run()
