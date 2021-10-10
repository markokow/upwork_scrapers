# packages
import scrapy
from scrapy.crawler import CrawlerProcess
import urllib
'''USING CRAWLERA PROXY'''

# scraper class
class Colleges(scrapy.Spider):
    # scraper name
    name = 'formrequest'
    
    # base URL
    base_url = 'https://www.unspsc.org/search-code'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'
    }

    # proxies
    proxies = []
    current_proxy = 0
    
    # crawler's entry point
    def start_requests(self):        
        # crawl pages        
        yield scrapy.Request(url=self.base_url, headers=self.headers, callback=self.parse)
    
    # parse response
    def parse(self, response, **kwargs):

        _eventtarget = response.css('input[id=__EVENTTARGET]::attr(value)').get()
        _eventargument = response.css('input[id=__EVENTARGUMENT]::attr(value)').get()
        _viewstate = response.css('input[id=__VIEWSTATE]::attr(value)').get()
        _viewstategenerator = response.css('input[id=__VIEWSTATEGENERATOR]::attr(value)').get()
        __VIEWSTATEENCRYPTED = response.css('input[id=__VIEWSTATEENCRYPTED]::attr(value)').get()
        _search_code = response.css('input[id="dnn$ctr1535$UNSPSCSearch$txtsearchCode"]::attr(value)').get()
        _search_title = 'test'
        _search = 'Search'
        _scrolltop = response.css('input[id=ScrollTop]::attr(value)').get()
        __dnnVariable = response.css('input[id=__dnnVariable]::attr(value)').get()
        __RequestVerificationToken = response.css('input[name=__RequestVerificationToken]::attr(value)').get()
        
        _payload = {
            '__EVENTTARGET':_eventtarget if _eventtarget else '',
            '__EVENTARGUMENT':_eventargument,
            '__VIEWSTATE':_viewstate,
            '__VIEWSTATEGENERATOR':_viewstategenerator,
            '__VIEWSTATEENCRYPTED':__VIEWSTATEENCRYPTED,
            'dnn$ctr1535$UNSPSCSearch$txtsearchCode':_search_code if _search_code else '',
            'dnn$ctr1535$UNSPSCSearch$txtSearchTitle':_search_title,
            'dnn$ctr1535$UNSPSCSearch$btnSearch':_search if _search else '',
            'ScrollTop':_scrolltop if _scrolltop else ' ',
            '__dnnVariable':__dnnVariable,
            '__RequestVerificationToken':__RequestVerificationToken,
        }

        # print(_payload)

        yield scrapy.FormRequest(response.url, formdata = _payload, callback = self.parse_child)

    
    def parse_child(self, response):

        # pass


        print(response.text)

        with open('res2.html', 'w', encoding='utf-8') as file:
            file.write(response.text)