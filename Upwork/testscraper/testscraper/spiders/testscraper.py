# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import requests
import json
import urllib

'''USING CRAWLERA PROXY'''

# scraper class
class Colleges(scrapy.Spider):
    # scraper name
    name = 'testscraper'
    
    # base URL
    base_url = 'https://www.mobile.de'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'
    }
    
    # # proxies
    # proxies = []
    # current_proxy = 0
    
    # crawler's entry point
    def start_requests(self):        
        # crawl pages        
        yield scrapy.Request(url=self.base_url, headers=self.headers, callback=self.parse)
    

    def parse(self, response, **kwargs):

        with open("test.html", "w", encoding='utf-8') as file:
            file.write(response.text)

        print(response.text)