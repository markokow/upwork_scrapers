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

class Brainly_Scrapy(scrapy.Spider):
    name = 'Brainly_Scrapy'
    currentPost = []
    part: int = 1
    idx: int = 0
    limit: int = 20
    today = str(datetime.datetime.now()).split('.')[0].replace('-', '_').replace(':', '_').replace(' ', '_')
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
            # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/78.0.3904.70 Safari/537.36',
            # 'Accept': 'application/json',
            # 'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Referer': 'https://brainly.com/subject/history',
            # 'content-type': 'application/json',
            # 'Connection': 'keep-alive',
            # 'Cookie': 'datadome=.5iNeTIResH_IF1LXZ9ko9~LVNXkc9K4hE83arKJ26Vg4k5nKqKSGuZNah-kuiZD-ze_~JULsHGniLKw6UbqE1PPhzopr6lBTLuNmbSd8.FNUxr6FK~Q28C2m5cgcpK0; Zadanepl_cookie[Token][Guest]=cDGMeVRKq2RiRH7aWXr2Ba6vSwoyfjTdlbKE4qGOZFpjSeXRu5MWvH57E4JV9NZupixVei8l3NC0T9bb; didomi_token=eyJ1c2VyX2lkIjoiMTgxYWRiNDktNDU4YS02MzhmLWJkZDAtMmM4ZDQ0ZjE4MWE3IiwiY3JlYXRlZCI6IjIwMjItMDYtMjlUMDQ6MjU6MDEuNzk2WiIsInVwZGF0ZWQiOiIyMDIyLTA2LTI5VDA0OjI1OjAxLjc5NloiLCJ2ZXJzaW9uIjpudWxsfQ==; g_state={"i_p":1656483943092,"i_l":1}; G_ENABLED_IDPS=google; Zadanepl_cookie[infobar]=',
            # 'Sec-Fetch-Dest': 'empty',
            # 'Sec-Fetch-Mode': 'cors',
            # 'Sec-Fetch-Site': 'same-origin'
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
        url = "https://brainly.com/graphql/us?operationName=feed&variables={\"gradeIds\":[],\"subjectIds\":[5],\"statusId\":\"ALL\",\"cursor\":null,\"feedType\":\"PUBLIC\",\"first\":20}&extensions={\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"a18dcee8ff57280c79a46e830df335650f7c74a60266dceb332a055b8a315b16\"}}"
        yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response, **kwargs):  # sourcery skip: avoid-builtin-shadow, low-code-quality
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
                    yield scrapy.Request(url=url, callback=self.parse_innerlink, headers=self.headers, meta = {'url': url})

        if nextCursor:
            cursor_string = f"\"{nextCursor}\""
            next_url = "https://brainly.com/graphql/us?operationName=feed&variables={\"gradeIds\":[],\"subjectIds\":[5],\"statusId\":\"ALL\",\"cursor\":" + cursor_string + ",\"feedType\":\"PUBLIC\",\"first\":20}&extensions={\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"a18dcee8ff57280c79a46e830df335650f7c74a60266dceb332a055b8a315b16\"}}"
            time.sleep(3)
            yield scrapy.Request(url=next_url, callback=self.parse, headers=self.headers)

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
        
    def close(self, reason):
        if ((self.idx) % self.limit) != 0:
            df = pd.DataFrame(self.url_list)
            df.to_csv(f'{self.today}_part{self.part}.csv', encoding='latin-1')
        
from scrapy.cmdline import execute

execute('scrapy runspider brainly_scrapy_v2.py'.split())