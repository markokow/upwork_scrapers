from inspect import indentsize
import scrapy
from scrapy.crawler import CrawlerProcess
import json

class OLX(scrapy.Spider):

    name = 'india_olx'

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}

    custom_settings = {
        'FEED_FORMAT' : 'csv',
        'FEED_URI': 'olx_india.csv'
    }

    def start_requests(self):

        for x in range(0, 5):
            _url = f'https://www.olx.in/api/relevance/v2/search?facet_limit=100&lang=en&location=1000001&location_facet_limit=20&page={str(x)}&platform=web-desktop&query=for%20sale%20house%20apartment&spellcheck=true'
            yield scrapy.Request(url=_url, headers=self.headers, callback=self.parse)

    def parse(self, response, **kwargs):

        _data  = json.loads(response.text)

        for _dat in _data['data']:

            _data_dict: dict = {}

            _id = _dat['id'].strip()
            _title = _dat['title'].strip()
            _price = _dat['price']['value']['display'].strip()
            _descrip = _dat['description'].strip()

            _data_dict['id'] = _id.encode('ascii', errors = 'ignore')
            _data_dict['title'] = _title.encode('ascii', errors = 'ignore')
            _data_dict['price'] = _price.encode('ascii', errors = 'ignore')
            _data_dict['description'] = _descrip.encode('ascii', errors = 'ignore')

            yield _data_dict



if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(OLX)
    process.start()
