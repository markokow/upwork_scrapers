# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import requests
import json
import urllib
from typing import List

class LoopNet(scrapy.Spider):
    # scraper name
    name = 'loopnet'
    
    # base URL
    base_url = 'https://www.loopnet.com/search/industrial-properties/los-angeles-ca/for-sale/?sk=fdb43a4d0f238b9261954e2d6a7b3daa&bb=oip4u-k_tNjwwsjz7D'
    # base_url = 'https://www.loopnet.com/Listing/1312-1316-Westwood-Blvd-Los-Angeles-CA/23924895/'
    
    # custom headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    }

    parsed_urls: List = []

    
    # crawler's entry point
    def start_requests(self):

        yield scrapy.Request(url=self.base_url, headers=self.headers, meta=None, callback=self.parse_listing)

    def parse(self, response, **kwargs):

        _urls = response.css('a::attr(href)').getall()

        for _url in _urls:

            if '/www.loopnet.com/Listing/' in _url:
                if _url in self.parsed_urls:
                    continue
                else:
                    self.parsed_urls.append(_url)
                    print(_url)
                    yield scrapy.Request(url=_url, headers=self.headers, meta=None, callback=self.parse)


        _next_page = response.css('a.beforeellipsisli::attr(href)').get()

        if _next_page is not None:
            yield scrapy.Request(url=_next_page, headers=self.headers, meta=None, callback=self.parse)
        else:
            print("Number of urls", len(self.parsed_urls))
            pass
    
    def parse_listing(self, response, **kwargs):

        # print(response.text)

        # with open("resp_text.html", "w") as file:
                # file.write(response.text)

        _agent_first_name = response.css('.contact-name > span:nth-child(1)::text').get()
        _agent_last_name = response.css('.contact-name > span:nth-child(2)::text').get()
        _agent_address = response.css('span.inline-block::text').getall()
        _company_name = response.css('.company-name-no-image::text').get()
        _telephone_number = response.css('.cta-phone-number > a:nth-child(2)::attr(href)').get()
        _loopnet_link = response.url
        _property_address = response.css('h1.breadcrumbs__crumb::text').get()
        _price = response.css('div.profile-hero-heading-wrap:nth-child(2) > div:nth-child(1) > h2:nth-child(2) > span:nth-child(4)::text').get()
        try:
            _price = _price if _price.startswith('$') else None
        except:
            _price = None
        # _parcel_number = response.css('table.property-data:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > span:nth-child(1)::text').get()

        _features = {
            'Agent First Name': _agent_first_name,
            'Agent Last Name': _agent_last_name,
            'Agent Address': ' '.join(_agent_address),
            'Company Name': _company_name,
            'Telephone Number': _telephone_number,
            'Loopnet Link': _loopnet_link,
            'Address': _property_address,
            'Price': _price,
        }

        # _property_data = response.css('table.featured-grid:nth-child(1)')
        # _tbody = _property_data.css('tbody')
        # _trs = _property_data.css('tr')

        # print(_tbody)

        # for _tr in _trs:
        #     print(_tr)
        #     # print(_tr.css('td::text')).getall()

        # print(_property_data)




        yield _features

    
    
    