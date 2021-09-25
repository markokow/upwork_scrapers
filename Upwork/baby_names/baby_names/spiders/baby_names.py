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
class BabyNames(scrapy.Spider):
    # scraper name
    name = 'babynames'
    
    # base URL
    base_url = 'https://www.babycenter.in/t1003021/baby-name-search-results?'
    
    # custom headers
    headers = {
        # 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # proxies
    proxies = []
    current_proxy = 0
    
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

        _data = response.css('#bnResults')

        _rows = _data.css('div.row')

        for _row in _rows[1:]:

            _name = _row.css('div:nth-child(2) > a:nth-child(1)::text').get()
            _gender = _row.css('div:nth-child(3)::text').get()
            _origin = _row.css('div:nth-child(4)::text').get()

            _features = {
                'name': _name.strip(),
                'gender': _gender.strip(),
                'origin': _origin.strip()
            }

            yield _features

            try:
                _next = response.css('.pgNext::attr(href)').get()


                yield scrapy.Request(url=self.base_url[:-1] + _next, headers=self.headers, callback=self.parse)
            except:
                pass