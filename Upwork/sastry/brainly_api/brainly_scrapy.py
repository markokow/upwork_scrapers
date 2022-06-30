import datetime
import scrapy
import pandas as pd
import json
from typing import List

class Brainly_Scrapy(scrapy.Spider):
    name = 'Brainly_Scrapy'
    currentPost = []
    part: int = 1
    idx: int = 0
    limit: int = 20
    today = str(datetime.datetime.now()).split('.')[0].replace('-', '_').replace(':', '_').replace(' ', '_')
    headers = {
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0'
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    url_list: List = []

    def start_requests(self):        
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

execute('scrapy runspider brainly_scrapy.py'.split())