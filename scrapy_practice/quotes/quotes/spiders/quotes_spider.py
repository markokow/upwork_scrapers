from typing import AsyncGenerator
import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']


    def parse(self, response, **kwargs):

        all_div_quotes = response.css('.quote')

        for quote in all_div_quotes: vb

            _quote = quote.css('.text::text').extract()
            _author = quote.css('.author::text').extract()
            _tag = quote.css('.tag::text').extract()

            yield {
                'quotes':_quote,
                'author': _author,
                'tag': _tag
                }
        # return super().parse(response, **kwargs)