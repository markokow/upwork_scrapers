# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from urllib.parse import urlencode
import requests
import json
import urllib

API = '89f53273207f9aacdce3069e17dfceb0'                        ##Insert Scraperapi API key here. Signup here for free trial with 5,000 requests: https://www.scraperapi.com/signup


def get_url(url):
    payload = {'api_key': API, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

# scraper class
class Json(scrapy.Spider):
    # scraper name
    name = 'json'
    
    # base URL
    base_url = 'https://shopee.ph/emocase-Lovely-Pineapple-Bird-Inflatable-Float-Drink-Can-Cup-Holder-Swimming-Party-Props-i.282998795.9556064677?position=9'
    
    # custom headers
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    # }

    
    # crawler's entry point
    def start_requests(self):

        yield scrapy.Request(url = get_url(self.base_url), callback=self.parse)

    # parse response
    def parse(self, res):

        _product_name = res.css('.attM6y > span:nth-child(2)::text').get()
        _product_link = res.url
        _product_category = res.css('div._1J-ojb:nth-child(2) > span:nth-child(7)::text').get()

        _features = {
            'product name': _product_name,
            'product link': _product_link,
            'product category': _product_category,
        }


        print(_features)