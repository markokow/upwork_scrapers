#packages
import scrapy
import urllib
import json
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector


#zillow class
class ZillowScraper(scrapy.Spider):

    name = 'zillow'

    Base_url = 'https://www.zillow.com/atlanta-ga/land/2_p/?'

    params = {
     'searchQueryState': '{"pagination":{"currentPage":2},"usersSearchTerm":"atlanta ga","mapBounds":{"west":-84.86089261132 813,"east":-84.10008938867188,"south":33.52835520920972,"north":34.0192115324712 4},"regionSelection":[{"regionId":37211,"regionType":6}],"isMapVisible":True,"fi lterState":{"doz":{"value":"30"},"sort":{"value":"globalrelevanceex"},"ah":{"val ue":True},"sf":{"value":False},"con":{"value":False},"mf":{"value":False},"manu" :{"value":False},"tow":{"value":False},"apa":{"value":False},"apco":{"value":False}},"isListVisible":True,"mapZoom":11}'

    }
 
    pass

    def start_requests(self):

        for _page in range (1,2):
            # parse params
            _parsed = json.loads(self.params['searchQueryState'])

            #
            print(_parsed)
            break

        return super().start_requests()


#main driver
if __name__ == "__main__":

    process = CrawlerProcess()
    process.crawl(ZillowScraper)
    process.start()




