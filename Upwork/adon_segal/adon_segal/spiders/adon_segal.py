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

'''USING CRAWLERA PROXY'''

# scraper class
class Adon_Segal(scrapy.Spider):
    # scraper name
    name = 'adon_segal'
    
    # base URL
    base_url = 'https://www.crompton.co.in/wp-admin/admin-ajax.php?action=getDealerCenters&service_center_state='
    # base_url = 'https://www.crompton.co.in/wp-admin/admin-ajax.php?action=getDealerCenters&service_center_state=Andhra%20Pradesh&startLimit=0&endLimit=1000'

    _limits = '&startLimit=0&endLimit=1000000'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    
    # crawler's entry point
    def start_requests(self):        
        # crawl pages        

        _states = ['Andaman And Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra And Nagar Hav.','Daman And Diu','Delhi',
        'Goa','Gujarat','Haryana','Himachal Pradesh','Jammu And Kashmir','Jharkhand','Karnataka','Madhya Pradesh','Maharashtra','Manipur','Meghalaya',
        'Mizoram','Nagaland','Odisha','Punjab','Rajasthan','Tamilnadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bangel','West Bengal']
        # _states = ['Uttar Pradesh']
        for _state in _states:

            for val in range(0,500,21):

                _url = self.base_url + _state.replace(' ', '%20') + '&startLimit=' + str(val) + '&endLimit=' + str(val+21)
                # _url = self.base_url + _state.replace(' ', '%20') + '&startLimit=' + str(126) + '&endLimit=' + str(147)

                yield scrapy.Request(url=_url, headers=self.headers, meta = {'state':_state}, callback=self.parse)

    # parse response
    def parse(self, res):

        _features: dict = {}
        _data: list = []

        _namepattern = r"<p class=\\\"shop-name\\\">.{0,100}<\\/p>"
        _names = re.findall(_namepattern, res.text)

        _addresspattern = r"<p>.{0,300}<\\/p>\\n"
        _address = re.findall(_addresspattern, res.text)

        _numberspattern = r"<span class=\\\"call-icon\\.{0,300}<\\/a><\\/li>"
        _numbers = re.findall(_numberspattern, res.text)
        _parsed_nums: list = []

        _emailspattern = r"<span class=\\\"gettouch\\\".{0,300}coustomerservice"
        _emails = re.findall(_emailspattern, res.text)
        _parsed_emails: list = []

        for val in _numbers:
            pattern = r"\d{9,100}"
            num = re.findall(pattern, val)
            num = [x.replace(',','').strip() for x in num]
            if not num:
                _parsed_nums.append("No data")
            else:
                _parsed_nums.append('\n'.join(num))

        for val in _emails:
            pattern = r"[0-9a-zA-Z-_.]+@\w+.com"
            email = re.findall(pattern, val)

            if not email:
                _parsed_emails.append("No data")
            else:
                _parsed_emails.append(email[-1].strip())
        
        for a,b,c,d in zip(_names, _address, _parsed_nums, _parsed_emails):

            _features = {
                'state': res.meta.get('state'),
                'name': a.split('<p class=\\"shop-name\\">')[-1].split('<\\')[0],
                'address': b.split('<p>')[-1].split('<\\')[0],
                'number': c,
                'email': d,
            }
            
            yield _features