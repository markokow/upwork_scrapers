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
    name = 'googlemapsv2'
    
    # base URL
    # base_url = 'https://www.google.com/maps/search/spa+in+newyork+usa/@40.7528097,-73.9234101,13z/data=!3m1!4b1'
    base_url = 'https://www.google.com/maps/preview/place?authuser=0&hl=en&gl=ph&pb=!1m18!1s0x89c25907ea1ef903:0xe4a0420198c04d76!2s!3m12!1m3!1d25564.62683895909!2d-73.92341015!3d40.75280965!2m3!1f0!2f0!3f0!3m2!1i1858!2i406!4f13.1!4m2!3d40.74591580852406!4d-73.98154735565186!6sspa+in+newyork+usa!13m50!2m2!1i408!2i240!3m2!2i10!5b1!7m42!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!2b1!4b1!9b0!14m4!1s1z5QYYuQMoXr-QaPh6_oAw!3b1!7e81!15i10555!15m40!1m6!4e2!18m3!3b0!6b0!14b0!20e2!2b1!4b1!5m5!2b1!3b1!5b1!6b1!7b1!10m1!8e3!17b1!20m2!1e3!1e6!24b1!25b1!26b1!29b1!30m1!2b1!36b1!43b1!52b1!55b1!56m2!1b1!3b1!65m5!3m4!1m3!1m2!1i224!2i298!22m1!1e81!29m0!30m1!3b1!32b1!37i574&q=*&pf=t'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }


    # crawler's entry point
    def start_requests(self):        

        yield scrapy.Request(url=self.base_url, headers=self.headers, callback=self.parse)
    
    # parse response
    def parse(self, res):
        # loop over college cards
        print(res)

        _data = json.loads(res.text)

        # print(json.dumps(_data, indent = 2))
