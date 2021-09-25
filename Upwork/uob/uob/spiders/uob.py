# packages
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json

class UOB(scrapy.Spider):
    # scraper name
    name = 'uob'
    # base URL
    base_url = 'https://www.uob.com.sg/personal/save/savings/singapore-dollar-time-fixed-deposits-rates.page'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0' 
    }

    def start_requests(self):        

        yield scrapy.Request(url=self.base_url, headers=self.headers, callback=self.parse)

    def parse(self, response, **kwargs):

        _data = response.css('#gld')

        for _count, _dat in enumerate(_data.css('tr')):
            if _count % 2 == 0:

                _month = _dat.css('td:nth-child(1) > p:nth-child(1) > strong:nth-child(1)::text').get()
                _interests = [_val.css('p::text').get() for _val in _dat.css('td')][1:5]

                for _count, _interest in enumerate(_interests):

                    if _count == 0:
                        _minimum = '-'
                        _maximum = '49,999'
                    elif _count == 1:
                        _minimum = '50,001'
                        _maximum = '249,999'
                    elif _count == 2:
                        _minimum = '250,000'
                        _maximum = '499,999'
                    else:
                        _minimum = '500,000'
                        _maximum = '999,999'
                    
                    _feature = {
                        'Tenure(months)': _month.split(' ')[0].strip(),
                        'Deposit(Minimum)': _minimum,
                        'Deposit (Maximum)': _maximum,
                        'Deposit Rate (% per annum)': _interest,
                    }

                    yield _feature
            else:
                continue