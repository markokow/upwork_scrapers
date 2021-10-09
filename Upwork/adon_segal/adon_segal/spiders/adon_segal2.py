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


'''USING CRAWLERA PROXY'''

API = '89f53273207f9aacdce3069e17dfceb0'                        ##Insert Scraperapi API key here. Signup here for free trial with 5,000 requests: https://www.scraperapi.com/signup


def get_url(url):
    payload = {'api_key': API, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)

    return proxy_url

# scraper class
class Adon_Segal(scrapy.Spider):
    # scraper name
    name = 'adon_segal2'
    
    # base URL
    base_url = 'https://www.maharashtradirectory.com/product/lighting-controllers.html'
    # base_url = 'https://www.upwork.com/ab/jobs/search/?page=2&q=web%20scrape&sort=recency'
    # base_url = 'https://www.crompton.co.in/wp-admin/admin-ajax.php?action=getDealerCenters&service_center_state=Andhra%20Pradesh&startLimit=0&endLimit=1000'

    _limits = '&startLimit=0&endLimit=1000000'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    }
    
    # crawler's entry point
    def start_requests(self):        
        # crawl pages        

            # for val in range(0,500,21):

            #     _url = self.base_url + _state.replace(' ', '%20') + '&startLimit=' + str(val) + '&endLimit=' + str(val+21)
            #     # _url = self.base_url + _state.replace(' ', '%20') + '&startLimit=' + str(126) + '&endLimit=' + str(147)
        # yield scrapy.Request(url=get_url(self.base_url), headers=self.headers,callback=self.parse)
        yield scrapy.Request(url=self.base_url, headers=self.headers,callback=self.parse)
    # parse response
    def parse(self, res):

        with open ("res2.html", "w") as file:

            file.write(res.text)

        print(res.text)

        # data = json.loads(res.text)

        # print(json.dumps(data, indent=2))