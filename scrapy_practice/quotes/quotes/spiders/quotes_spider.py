from typing import AsyncGenerator
import scrapy
from scrapy.crawler import CrawlerProcess

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']
    
    custom_settings = {
        'FEED_FORMAT' : 'csv',
        'FEED_URI': 'quotes.csv'
    }


    def parse(self, response, **kwargs):

        all_div_quotes = response.css('.quote')

        for quote in all_div_quotes: 

            _quote = quote.css('.text::text').extract_first()
            _author = quote.css('.author::text').extract_first()
            _tag = quote.css('.tag::text').get()

            yield {
                'quotes':_quote.encode('ascii', errors='ignore'),
                'author': _author.encode('ascii', errors='ignore'),
                'tag': _tag.encode('ascii', errors='ignore')
                }
        # return super().parse(response, **kwargs)


#run spider
process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()