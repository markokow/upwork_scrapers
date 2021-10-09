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
    name = 'adon_segal2'
    
    # base URL
    # base_url = 'https://www.havells.com/en/dealer-locator.html?State=UTTAR%20PRADESH&District=AGRA-UP&Product=Lighting'
    # base_url = 'https://www.havells.com/en/dealer-locator.html?State=UTTAR%20PRADESH'
    base_url = 'https://www.havells.com/en/dealer-locator.html?State='
    # base_url = 'https://www.upwork.com/ab/jobs/search/?page=2&q=web%20scrape&sort=recency'
    # base_url = 'https://www.crompton.co.in/wp-admin/admin-ajax.php?action=getDealerCenters&service_center_state=Andhra%20Pradesh&startLimit=0&endLimit=1000'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    }

    _legit_url = 'https://www.havells.com/en/dealer-locator.html?State=ANDHRA%20PRADESH&District=AMADALAVALASA-AP&Product=Lighting'
    
    # crawler's entry point
    def start_requests(self):        

        # states = csv.DictReader(open("states.csv"))
        locations = csv.DictReader(open("locations.csv"))

        for val in locations:
            state = val['state'].replace(' ', '%20')
            city = val['city'].replace(' ', '%20')

            _loc = {
                'state':  val['state'].strip(),
                'city': val['city'].strip()
            }

            print(_loc)

            url = self.base_url + str(state) + '&' + 'District=' + str(city) + '&Product=Lighting'

            yield scrapy.Request(url=url, headers=self.headers, meta = _loc, callback=self.parse)
            

    # parse response
    def parse(self, res):

        _stores = res.css('.dealerLocator > div.col-sm-6.gallery-col')

        for store in _stores:

            data = store.css('div.store-address ::text').getall()

            print(data)

            _name = data[2].strip() if data[2] is not None else 'No data'
            _full_address = data[4].strip() if data[4] is not None else 'No data'
            _town = data[6].strip() if data[6] is not None else 'No data'
            _district = data[7].strip() if data[7] is not None else 'No data'
            _city = data[8].strip() if data[8] is not None else 'No data'
            _postal_code = data[9].strip() if data[9] is not None else 'No data'
            _telephone = data[12].strip() if data[12] is not None else 'No data'
            _email = data[19].strip() if data[19] is not None else 'No data'

            try:
                _remarks = data[20].strip() if data[20] is not None else 'No data'
            except IndexError:
                _remarks = 'No data'

            _Features = {
                'name': _name,
                'address': _full_address,
                'town': _town,
                'district': _district.split('District : ')[-1],
                'city': _city.split('City : ')[-1],
                'state': res.meta.get('state'),
                'postal code': _postal_code.split('Postal Code : ')[-1],
                'telephone': _telephone.split('+')[-1],
                'email': _email,
                'remarks': _remarks,
            }

            yield _Features


        # cities = res.css('#p_lt_ctl03_pageplaceholder_p_lt_ctl00_Form_Galaxy_Locator_plcUp_form_City_dropDownList > option::text').getall()

        # for city in cities[1:]:

        #     _features = {
        #         'state': res.meta.get('state'),
        #         'city': city}

        #     # print(_features)

        #     yield _features
        #     # print(city)

        # data = json.loads(res.text)

        # print(json.dumps(data, indent=2))