from urllib import parse
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import headers
from scrapy.selector import Selector
import time
import json

class OnTheMarket(scrapy.Spider):
    name = 'market'
    # start_urls = ['http://quotes.toscrape.com/']

    allowed_domains = ['https://www.onthemarket.com']

    headers = {
        'Host': 'www.onthemarket.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'content-type': 'application/json; charset=utf-8',
        'Connection': 'keep-alive',
        'Referer': 'https://www.onthemarket.com/for-sale/property/london/',
        'Cookie': 'otm-tracking=w3kCdwuis3MdfbxgKnEWE%2BZ4Uwk2Wac063f%2B2xEfU06J3Q9vb93Jl%2FAltMSpBr1bT%2F8l8tIkWbx7CD0o%2BXxJOVjdq0EAoVUND5e4aQzoqaU%3D--ex4%2F8fWzZ5W0w9k%2FZ%2FrYfgLxkstW%2BBXjzXvzdYViUX0%3D; CookieControlTC=CPL_tYePL_tYeEDAJBENBqCsAP_AAH_AAAwIILtf_X__b3_n-_79__t0eY1f9_7_v-0zjhfdt-8N2f_X_L8X_2M7vF36pr4KuR4ku3bBIQdtHOncTUmx6olVrzPsbk2Mr7NKJ7Pkmnsbe2dYGH9_n93T_ZKZ7______7________________________-_____9____________9____-CC7X_1__29_5_v-_f_7dHmNX_f-_7_tM44X3bfvDdn_1_y_F_9jO7xd-qa-CrkeJLt2wSEHbRzp3E1JseqJVa8z7G5NjK-zSiez5Jp7G3tnWBh_f5_d0_2Sme______-_________________________v_____f____________f____gAAA; CookieControl={"consentDate":1630730704482,"interactedWith":true,"necessaryCookies":["otm-tracking","_gid","_ga","_gat","AMP_TOKEN","_gac_*","_gat_UA*","_dc_gtm_UA*","giosg_*"],"consentExpiry":90,"iabConsent":"CPL_tYePL_tYeEDAJBENBqCsAP_AAH_AAAwIILtf_X__b3_n-_79__t0eY1f9_7_v-0zjhfdt-8N2f_X_L8X_2M7vF36pr4KuR4ku3bBIQdtHOncTUmx6olVrzPsbk2Mr7NKJ7Pkmnsbe2dYGH9_n93T_ZKZ7______7________________________-_____9____________9____-CC7X_1__29_5_v-_f_7dHmNX_f-_7_tM44X3bfvDdn_1_y_F_9jO7xd-qa-CrkeJLt2wSEHbRzp3E1JseqJVa8z7G5NjK-zSiez5Jp7G3tnWBh_f5_d0_2Sme______-_________________________v_____f____________f____gAAA"}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cache-Control': 'max-age=0',
        'TE': 'trailers'
    }

    # custom_settings = {
    #     'FEED_FORMAT' : 'csv',
    #     'FEED_URI': 'market.csv'
    # }

    def start_requests(self):

        url = 'https://www.onthemarket.com/for-sale/property/london/'

        for val in range(0,5):
            _url = url + '?page=' + str(val)

            if val == 0:
                _url = url

            self.headers['Referer'] = _url

            yield scrapy.Request(url = _url, headers = self.headers, callback=self.parse)
            # time.sleep(2)

            


    def parse(self, response, **kwargs):

        time.sleep(3)

        # with open('res.html', 'w') as html_file:
        #     html_file.write(response.text)
        _units = response.css('li.result.property-result.panel.exclusive.new.first')

        for _unit in _units:

            _data_dict: dict = {}
            
            _title = _unit.css('.title a::text').get()
            _address = _unit.css('.address a::text').get()
            _price = _unit.css('.price::text').get()
            _numbers = _unit.css('a.call::attr(href)').get()
            _url = _unit.css('picture').css('img::attr(src)').get()

            _data_dict['title'] = _title
            _data_dict['address'] = _address
            _data_dict['price'] = _price.encode('ascii','ignore').decode('utf-8').strip()
            _data_dict['contact'] = _numbers
            _data_dict['url'] = _url

            # print(_data_dict)

            yield _data_dict

            print(json.dumps(_data_dict, indent = 2))
        
        # _next_url = 'https://www.onthemarket.com' + response.css('.arrow::attr(href)').get()

        # print('next_url', _next_url)

        # if _next_url is not None:
        #     yield scrapy.Request(url = _next_url, headers = self.headers, callback=self.parse)
        # else:
        #     pass

        # print(_prices)
        # print(type(_prices))

        # _price = _prices.css('a.price::text').get()

        # print(_price)



# #run spider
# if __name__ == '__main__':
#     process = CrawlerProcess()
#     process.crawl(OnTheMarket)
#     process.start()