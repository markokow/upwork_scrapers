# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import requests
import json
from urllib.parse import urljoin


'''USING CRAWLERA PROXY'''

# scraper class
class RedFin(scrapy.Spider):
    # scraper name
    name = 'autohero'

    # base URL
    base_url = 'https://www.browsenodes.com/'
    # base_url = 'https://www.browsenodes.com/amazon.com/browseNodeLookup/2864120011.html'
    
    # custom headers
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }   

    counter = 0
    
    # crawler's entry point
    def start_requests(self):        
                #print(next_proxy)
        yield scrapy.Request(url=self.base_url, headers=self.headers, meta = None, callback=self.parse)
    # parse response
    def parse(self, res):
        _data = res.text

        # print(_data)

        if 'no child node' in _data:
            self.counter+=1
            print("Count:", self.counter)
            yield res.meta

        else:
            _tbody = res.css('.table-striped > tbody:nth-child(2)')
            _trs = _tbody.css('tr')

            for _tr in _trs:
                _name = _tr.css('td::text').getall()[0]
                _id = _tr.css('td::text').getall()[1]
                _href = _tr.css('a.read-more::attr(href)').get()

                _features = {
                    'name': _name.strip(),
                    'id': _id.strip(),
                }

                if _href is not None:
                    _url = urljoin(self.base_url, _href)
                    yield scrapy.Request(url=_url, headers=self.headers,meta = _features, callback=self.parse)


