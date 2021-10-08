# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import requests
import json
import urllib
from urllib.parse import urlencode


'''USING CRAWLERA PROXY'''
API = '89f53273207f9aacdce3069e17dfceb0'                        ##Insert Scraperapi API key here. Signup here for free trial with 5,000 requests: https://www.scraperapi.com/signup


def get_url(url):
    payload = {'api_key': API, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)

    return proxy_url

# scraper class
class CanadianTire(scrapy.Spider):
    # scraper name
    name = 'canadiantire'
    
    # base URL
    base_url = 'https://www.canadiantire.ca/en/in-store-clearance.html?x1=HIDECROSSMERCH;q1=T;x2=s.store-has-clearance;q2=T;x3=ast-id-level-1;q3=kids-toys-games;adlocation=NavLinks_Clearance_DealsTab_en'
    # base_url = 'https://api-triangle.canadiantire.ca/esb/PriceAvailability?Product=0765893P%2C0505927P%2C0844088P%2C0506894P%2C0506309P%2C0500970P%2C0506332P%2C0506326P%2C0506351P%2C0506393P%2C0765898P%2C0508177P%2C0508067P%2C0500730P&Store=0452&Banner=CTR&isKiosk=FALSE&Language=E&_=1633395723610'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    

    # proxies
    proxies = []
    current_proxy = 0
    
    # crawler's entry point
    def start_requests(self):        
 
                #print(next_proxy)
        yield scrapy.Request(url=self.base_url, headers=self.headers, callback=self.parse)
        # yield scrapy.Request(url=get_url(self.base_url), callback=self.parse)

    
    # parse response
    def parse(self, res):

        with open ("res.html", "w") as file:

            file.write(res.text)

    