#packages
import scrapy
from scrapy import crawler
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector


#onthemarket scraper class

class OnTheMarket(scrapy.Spider):
    #spidern name
    name = 'onthemarket'

    base_url = 'https://www.onthemarket.com/for-sale/commercial/property/cr0/?radius=3.0'

    params = {
        'page': '0',
        'radius': '3.0'
    }

    #headers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}

    #custom download settings
    # custom_settings  = {

    # }

    def __init__(self, name, **kwargs):
        content = ''

    
        pass


if __name__ == '__main__':
    process = CrawlerProcess()
