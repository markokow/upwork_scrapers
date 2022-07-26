import requests
import io
from typing import List
from datetime import datetime
import json
import pandas as pd

class Brainly:
    def __init__(self, *, split_number: int = 100, API_KEY: str = '', parsed_urls: List = []) -> None:
        '''Initialize variables used for scraping.'''

        self.base_url: str = "https://brainly.com/graphql/us?operationName=feed&variables=%7B\"gradeIds\"%3A[]%2C\"subjectIds\"%3A[5]%2C\"statusId\"%3A%22ALL\"%2C\"cursor\"%3A%22Y3Vyc29yOjE2NTY1Njg2MTU%3D\"%2C\"feedType\"%3A%22PUBLIC\"%2C\"first\"%3A20%7D&extensions=%7B%22persistedQuery\"%3A%7B%22version\"%3A1%2C\"sha256Hash\"%3A\"a18dcee8ff57280c79a46e830df335650f7c74a60266dceb332a055b8a315b16\"%7D%7D"
        self.result: List = []
        self.current_url: str = ''
        self.parsed_urls: List = parsed_urls

        self.API_KEY: str = API_KEY
        self.split_number: int = split_number
        self.today = str(datetime.now()).split('.')[0].replace('-', '_').replace(':', '_').replace(' ', '_')
        self.idx: int = 0
        self.part: int = 1

        self.result: List = []

    def fetch(self):
        '''Fetch the url and returns bs4 object.'''
        print(f"current url: {self.current_url}")
        payload = {'api_key': self.API_KEY, 'url': self.current_url}
        response = requests.get('http://api.scraperapi.com', params=payload, timeout=60)

        return response

    def parse(self, *, response) -> str:
        '''Parse the urls contained in the page and append to results.'''
        data = json.loads(response.text)

        try:
            nextCursor = data["data"]["feed"]["pageInfo"]["endCursor"]
        except Exception:
            nextCursor = None

        if data:
            if edges := data["data"]["feed"]["edges"]:
                for _ in edges:
                    id = _["node"]["databaseId"]
                    url =  f"https://brainly.com/question/{id}?answeringSource=feedPublic/homePage/1"
                    title = _["node"]["content"]
                    if title:
                        title = title.strip()
                        title = title.replace('<br />', '')
                        title = title.replace('\n', ' ')
                        try:
                            title = f'{title[:90]}...'
                        except:
                            pass

                    try:
                        title = title.encode('MacRoman').decode('utf-8') 
                    except:
                        pass


                    if url not in self.parsed_urls:
                        self.parsed_urls.append(url)
                        self.result.append(
                            {'url': url,
                            'title': title}
                        )

                        with open("parsed_urls.txt", 'w') as f:
                            for item in self.parsed_urls:
                                f.write("%s\n" % item)

                        self.idx += 1

                        if ((self.idx) % self.split_number) == 0:
                            df = pd.DataFrame(self.result)
                            df.to_csv(f'{self.today}_part{self.part}.csv', encoding='utf-8')
                            print(f'{self.today}_part{self.part}.csv saved to folder.')
                            self.result = []
                            self.part += 1

        if nextCursor:
            cursor_string = f"\"{nextCursor}\""
            next_url = "https://brainly.com/graphql/us?operationName=feed&variables={\"gradeIds\":[],\"subjectIds\":[5],\"statusId\":\"ALL\",\"cursor\":" + cursor_string + ",\"feedType\":\"PUBLIC\",\"first\":20}&extensions={\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"a18dcee8ff57280c79a46e830df335650f7c74a60266dceb332a055b8a315b16\"}}"
            self.current_url = next_url

            while True:
                try:
                    response = self.fetch()
                    self.parse(response=response)
                    break
                except json.JSONDecodeError:
                    continue


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
  
    
    def run(self):
        '''Run all cases using the urls'''
        # print("Scraping is running please don't exit...")
        self.current_url = 'https://brainly.com/graphql/us?operationName=feed&variables=%7B%22gradeIds%22:[],%22subjectIds%22:[5],%22statusId%22:%22ALL%22,%22cursor%22:null,%22feedType%22:%22PUBLIC%22,%22first%22:20%7D&extensions=%7B%22persistedQuery%22:%7B%22version%22:1,%22sha256Hash%22:%22a18dcee8ff57280c79a46e830df335650f7c74a60266dceb332a055b8a315b16%22%7D%7D'
       
        try:
            while True:
                try:
                    response = self.fetch()
                    self.parse(response=response)
                    break
                except json.JSONDecodeError:
                    continue
        except KeyboardInterrupt:
            pass
        finally:

            if ((self.idx) % self.split_number) != 0:
                df = pd.DataFrame(self.result)
                df.to_csv(f'{self.today}_part{self.part}.csv', encoding='utf-8')
                print(f'{self.today}_part{self.part}.csv saved to folder.')

        
            

if __name__ == '__main__':
    '''Run main file.'''
    split_number: int = 10
    API_KEY: str = 'c02e4baee09252c02af2157e51fe4547'

    parsed_urls: List = []

    try:
        with open('parsed_urls.txt') as f:
            parsed_urls = [_.strip() for _ in f.readlines()]

    except FileNotFoundError:
        f= open("parsed_urls.txt","w+")
        f.close()
    
    #Run scraper
    scraper = Brainly(split_number = split_number, API_KEY=API_KEY, parsed_urls = parsed_urls)
    scraper.run()
