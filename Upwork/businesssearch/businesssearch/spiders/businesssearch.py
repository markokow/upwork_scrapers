# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import requests
import json
import urllib

'''USING CRAWLERA PROXY'''

# scraper class
class BusinessSearch(scrapy.Spider):
    # scraper name
    name = 'businesssearch'
    
    # base URL
    base_url = 'https://businesssearch.sos.ca.gov/CBS/SearchResults?filing=&SearchType=CORP&SearchCriteria=1&SearchSubType=Keyword'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    

    # proxies
    proxies = []
    current_proxy = 0
    
    # crawler's entry point
    def start_requests(self):        
        yield scrapy.Request(url=self.base_url, headers=self.headers, callback=self.parse)
    # parse response
    def parse(self, res):

        _trs = res.css('#enitityTable > tbody:nth-child(2) > tr')

        for _tr in _trs:

            _data = _tr.css('td::text').getall()

            _entity_number =_data[0].strip()
            _regitration_date = _data[1].strip()
            _status = _data[2].strip()
            _entity_name = _tr.css('td > button.btn-link.EntityLink::text').get().strip()
            _jurisdiction = _data[6].strip()
            _agent = _data[7].strip()

            _features = {
                'entity_number': _entity_number,
                'registration_date': _regitration_date,
                'status': _status,
                'entity_name': _entity_name,
                'jurisdiction': _jurisdiction,
                'agent_for_service_of_process': _agent,
            }

            yield _features

            _button = _tr.css('td > button.btn-link.EntityLink')

            print(_button)

            # # print(_data)s
            # for _val in _data:
            #     print(_val.strip())
            break

        print("LEN IS", len(_trs))

        # print(res.text)

    def parse_child(self, res):
        pass



# # main driver
# if __name__ == '__main__':
#     # run scraper
#     process = CrawlerProcess()
#     process.crawl(BusinessSearch)
#     process.start()
    
    
    