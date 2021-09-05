import scrapy
from scrapy.crawler import CrawlerProcess
import json
import csv

class Pharmeasy(scrapy.Spider):
    name = 'pharmeasy'

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    'Cookie': 'X-App-Version=2.1; X-Phone-Platform=web; X-IP=124.106.142.220%2C%20202.138.177.20%2C%2023.55.246.84; X-Default-City=1; X-Pincode=400001; XdI=0e8e9f8249fae49f04ea1e96a61f63b6; XPESS=active; XPESD={%22session_id%22:%22s_w_0e8e9f8249fae49f04ea1e96a61f63b6_1630809798000%22%2C%22session_id_flag%22:%22fingerprint%22%2C%22referrer%22:%22https://www.youtube.com/%22%2C%22session_start_time%22:%222021-09-05T02:43:18.603Z%22}; pe_last_active=Sun%20Sep%2005%202021%2010:46:29%20GMT+0800%20(Philippine%20Standard%20Time)'
    }

    custom_settings = {
        'FEED_FORMAT' : 'csv',
        'FEED_URI': 'pharma.csv'
    }

    base_url = 'https://pharmeasy.in/api/otc/getCategoryProducts?categoryId=89&page='


    def start_requests(self):

        page = 2

        for page in range (1, 5):
            next_page = self.base_url + str(page)

            yield scrapy.Request(url=next_page, headers= self.headers, callback= self.parse)

    def parse(self, response, **kwargs):

            _data_dict: dict = {}

            _data = json.loads(response.text)

            _products = _data['data']['products']

            for _prod in _products:

                _data_dict['name'] = _prod['name']
                _data_dict['slug'] = _prod['slug']
                _data_dict['manufacturer'] = _prod['manufacturer']
                _data_dict['price'] = _prod['salePriceDecimal']
                _data_dict['availability'] = _prod['productAvailabilityFlags']['isAvailable']
                _data_dict['images'] = ', '.join(_prod['images'])


                # print(type(_prod['images']))

                print(_data_dict)
                yield _data_dict



if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Pharmeasy)
    process.start()
