# packages
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import requests
import json
import urllib

'''USING CRAWLERA PROXY'''

# scraper class
class MacBetBookMakers(scrapy.Spider):
    # scraper name
    name = 'macbetbookmakers'
    
    # base URL
    base_url = 'https://data.macbet.cloudbetservices.com/graphql'
    
    # custom headers
    headers = {
'X-Firefox-Spdy':	'h2',
'access-control-allow-origin':'*',
'content-encoding':	'gzip',
'content-length':	'1612',
'content-type':	'application/json; charset=utf-8',
'date':	'Sat, 25 Sep 2021 10:32:50 GMT',
'etag':	'W/"4b25-c0k2Ol8S49Fn4LygQb/uxoDRR0Y"',
'vary':	'Accept-Encoding',
'x-powered-by':	'Express',
    }

    
    # crawler's entry point
    def start_requests(self):        
        # crawl pages        
        _url = self.base_url + 'startIndex=' + str(0) + '&startsWith=' + str('a')

        yield scrapy.Request(url=_url, headers=self.headers, callback=self.parse)
        
        # for page in range(0, 121, 40):

        #     _letter = 'a'
        #     try:
        #         _url = self.base_url + 'startIndex=' + str(page) + '&startsWith=' + str(_letter)

        #         yield scrapy.Request(url=_url, headers=self.headers, callback=self.parse)

        #     except Exception as e:
        #         continue
        # # https://www.babycenter.in/t1003021/baby-name-search-results?startIndex=0&startsWith=a
    
    # parse response
    def parse(self, response, **kwargs):

        _data = json.loads(response.text)

        print(json.dumps(_data, indent=2))