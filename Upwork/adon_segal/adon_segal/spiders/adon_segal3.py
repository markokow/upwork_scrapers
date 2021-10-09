# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import requests
import json
import urllib
from bs4 import BeautifulSoup
import re
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import csv


'''USING CRAWLERA PROXY'''

API = '89f53273207f9aacdce3069e17dfceb0'                        ##Insert Scraperapi API key here. Signup here for free trial with 5,000 requests: https://www.scraperapi.com/signup


def get_url(url):
    payload = {'api_key': API, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)

    return proxy_url

# scraper class
class Adon_Segal(scrapy.Spider):
    # scraper name
    name = 'adon_segal3'
    
    base_url = 'https://www.deldure.com/s?query=wipro+lighting+distributors&page=1&state=andaman+and+nicobar+islands&city=port+blair&country=india'

    allowed_domains = ["https://www.deldure.com"]


    headers = {
# 'Host': 'www.deldure.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# 'Accept-Language': 'en-US,en;q=0.5',
# 'Accept-Encoding': 'gzip, deflate, br',
# 'Alt-Used': 'www.deldure.com',
# 'Connection': 'keep-alive',
# 'Cookie': 'JSESSIONID=o2IB_8-oiOhsiEZdyTjt9ZO0xGOsBgJ2a5r925n-.localhost',
# 'Upgrade-Insecure-Requests': '1',
# 'Sec-Fetch-Dest': 'document',
# 'Sec-Fetch-Mode': 'navigate',
# 'Sec-Fetch-Site': 'same-origin',
'Cache-Control': 'max-age=0',

    }

    
    # crawler's entry point
    def start_requests(self):        

        yield scrapy.Request(url=self.base_url, headers=self.headers, callback=self.parse)
            

    # parse response
    def parse(self, res):
        print(res.text)

        with open ('deldure1.html', 'w') as file:

            file.write(res.text)