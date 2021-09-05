import scrapy
from scrapy.crawler import CrawlerProcess


class UrbanDictionary(scrapy.Spider):
    name = 'urban'

    _url = 'https://www.urbandictionary.com/popular.php?character=B'

    _headers = {
                'Host': 'www.urbandictionary.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Cookie': 'usprivacy=1---; OptanonConsent=isIABGlobal=false&datestamp=Sun+Sep+05+2021+16%3A02%3A23+GMT%2B0800+(Philippine+Standard+Time)&version=6.2.0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&hosts=&legInt=&AwaitingReconsent=false&geolocation=PH%3B40; country_code=PH; OptanonAlertBoxClosed=2021-09-05T08:02:23.641Z; OneTrustWPCCPAGoogleOptOut=true',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1'
    }


    def start_requests(self):

        yield scrapy.Request(url = self._url, headers= self._headers, callback=self.parse)


        # return super().start_requests()
    def parse(self, response, **kwargs):

        _list = response.css('ul.no-bullet')

        _links = [_li.css('a::attr(href)').get() for _li in _list.css('li')]

        for val in _links:
            print(val)
        '''Extract data.'''


        # return super().parse(response, **kwargs)






if __name__ == '__main__':

    process = CrawlerProcess()
    process.crawl(UrbanDictionary)
    process.start()