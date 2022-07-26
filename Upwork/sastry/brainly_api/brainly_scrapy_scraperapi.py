import datetime
import scrapy
import pandas as pd
import json
from typing import List
from bs4 import BeautifulSoup
import requests
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import time
from urllib.parse import urlencode

class Brainly_Scrapy(scrapy.Spider):
    name = 'Brainly_Scrapy'
    currentPost = []
    part: int = 1
    idx: int = 0
    limit: int = 20
    today = str(datetime.datetime.now()).split('.')[0].replace('-', '_').replace(':', '_').replace(' ', '_')
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0',
    }
    # headers: dict = {}
    url_list: List = []

    def get_useragent(self):
        '''Gets the user agent using the os.'''
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=1000)
        return user_agent_rotator.get_random_user_agent()

    def start_requests(self):  
        # page = requests.get('https://www.whatismybrowser.com/detect/what-is-my-user-agent/')
        # soup = BeautifulSoup(page.text, 'lxml')
        # print(soup)
        # user_agent = soup.find("div", {"id": "detected_value"}) 
        # user_agent = 
        # self.headers = {'User-Agent':self.get_useragent()}
        # print("********************")
        # print(self.headers)  
        # print("********************")
        # url = "https://brainly.com/graphql/us?operationName=feed&variables={\"gradeIds\":[],\"subjectIds\":[5],\"statusId\":\"ALL\",\"cursor\":null,\"feedType\":\"PUBLIC\",\"first\":20}&extensions={\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"a18dcee8ff57280c79a46e830df335650f7c74a60266dceb332a055b8a315b16\"}}"
        API_KEY = '9dbc100070f87da569a02d0e6c609b26'
        URL_TO_SCRAPE = 'https://brainly.com/graphql/us?operationName=feed&variables=%7B%22gradeIds%22:[],%22subjectIds%22:[5],%22statusId%22:%22ALL%22,%22cursor%22:null,%22feedType%22:%22PUBLIC%22,%22first%22:20%7D&extensions=%7B%22persistedQuery%22:%7B%22version%22:1,%22sha256Hash%22:%22a18dcee8ff57280c79a46e830df335650f7c74a60266dceb332a055b8a315b16%22%7D%7D'
        payload = {'api_key': API_KEY, 'url': URL_TO_SCRAPE}
        url = "hhttp://api.scraperapi.com" + urlencode(payload)
        yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response, **kwargs):  # sourcery skip: avoid-builtin-shadow, low-code-quality
        data = json.loads(response.text)
        print(data)

        # try:
        #     nextCursor = data["data"]["feed"]["pageInfo"]["endCursor"]
        # except Exception:
        #     nextCursor = None

        # if data:
        #     if edges := data["data"]["feed"]["edges"]:
        #         for _ in edges:
        #             id = _["node"]["databaseId"]
        #             url =  f"https://brainly.com/question/{id}?answeringSource=feedPublic/homePage/1"
        #             yield scrapy.Request(url=url, callback=self.parse_innerlink, headers=self.headers, meta = {'url': url})

        # if nextCursor:
        #     cursor_string = f"\"{nextCursor}\""
        #     next_url = "https://brainly.com/graphql/us?operationName=feed&variables={\"gradeIds\":[],\"subjectIds\":[5],\"statusId\":\"ALL\",\"cursor\":" + cursor_string + ",\"feedType\":\"PUBLIC\",\"first\":20}&extensions={\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"a18dcee8ff57280c79a46e830df335650f7c74a60266dceb332a055b8a315b16\"}}"
        #     time.sleep(3)
        #     yield scrapy.Request(url=next_url, callback=self.parse, headers=self.headers)

    def parse_innerlink(self, response, **kwargs):
        url = response.meta.get('url')
        title = response.css('title::text').get()
        title = title.strip() if title else ''
        title = title.replace('- Brainly.com', '')
        title = title.strip()

        self.url_list.append(
            {'url': url,
            'title': title}
        )
        self.idx += 1

        if ((self.idx) % self.limit) == 0:
            df = pd.DataFrame(self.url_list)
            df.to_csv(f'{self.today}_part{self.part}.csv', encoding='latin-1')
            self.url_list = []
            self.part += 1
        
    # def close(self, reason):
    #     if ((self.idx) % self.limit) != 0:
    #         df = pd.DataFrame(self.url_list)
    #         df.to_csv(f'{self.today}_part{self.part}.csv', encoding='latin-1')
        
from scrapy.cmdline import execute

execute('scrapy runspider brainly_scrapy_scraperapi.py'.split())