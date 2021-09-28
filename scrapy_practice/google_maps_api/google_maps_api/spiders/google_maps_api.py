# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import googlemaps


'''USING CRAWLERA PROXY'''

# scraper class
class Colleges(scrapy.Spider):
    # scraper name
    name = 'google_maps'
    
    # base URL
    base_url = 'https://www.niche.com/colleges/search/all-colleges/?'
    
    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    api_key = 'AIzaSyB2iFtzGu9ZsAcPsCjpitx5cowopzlawvM'

    map_client = googlemaps.Client(api_key)
    

    # crawler's entry point
    def start_requests(self):        

        try:
            print("HEY")

            data = self.map_client.geocode('Lanxess Arena Köln')
            results = data.get('results')


            print(results)

        except Exception as e:
            print(e)


        # # crawl pages        
        # for page in range(1, 254):
        #     try:
        #         # next page
        #         next_page = self.base_url + urllib.parse.urlencode({'page': str(page)})

        #         #print(next_proxy)
        #         yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse)

        #     except Exception as e:
        #         print(e)
    
    # parse response
    def parse(self, res):

        pass
