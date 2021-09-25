# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import requests
import json
import urllib


class EudoNet(scrapy.Spider):


    name = 'eudonet'

    proxy = '94.76.137.2'

    headers = {

'Host': 'w12.eudonet.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'cross-site',
'Sec-Fetch-User': '?1',
'If-Modified-Since': 'Thu, 05 Aug 2021 20:20:20 GMT',
'If-None-Match': '"23e83750378ad71:0"',
'Cache-Control': 'max-age=0'
    }

    base_url = 'https://w12.eudonet.com/specif/eudo_07390/web/index.html#/tableauDesMembres'


    def start_requests(self):


        yield scrapy.Request(url=self.base_url, headers=self.headers, meta={'proxy': "https://147.135.255.62:8139"}, callback=self.parse)

    
    def parse(self, response, **kwargs):

        print(response.text)

