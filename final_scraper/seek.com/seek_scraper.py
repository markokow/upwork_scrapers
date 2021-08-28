import csv
import requests
from bs4 import BeautifulSoup
# import io
# from datetime import datetime
# from urllib.request import urlopen, Request
# import re

class ScrapeSeek():

    def __init__(self,):
        self.result = []
        self.base_url = 'https://www.seek.com.au'
        self.sort_mode = 'ListedDate'#KeywordRelevance

    def fetch(self, link):
        try:
            response = requests.get(link)
        except:
            print('Request denied.')

        return response

    def parse_data_child(self, child_link):
        print('Scraping url:', child_link)

        result = {}

        #Request html of child
        response = self.fetch(child_link)
        content = BeautifulSoup(response.text, features = "lxml")

        data = content.find_all('div', class_ = 'yvsb870 _14uh9942g _1lOnv_4')

        #Get data of child link
        result['Job Ad URL'] = child_link
        result['Job Ad Area'] = data[1].text
        result['Job Category'] = data[2].text
        result['Work Type'] = data[-1].text

        return result


    def parse_data_parent(self, response):
        result = []

        content = BeautifulSoup(response.text, features = "lxml")

        #Search for jobs in div with this class
        jobs = content.find('div', class_= '_1UfdD4q')

        for job in jobs:

            parent_dict = {}

            #Get all a and span attribute
            job_link = job.find('a', class_='_2S5REPk')
            advertiser_link = job.find('a', class_ = '_17sHMz8')
            short_description_link = job.find('span', class_ = '_2OKR1ql')
            job_location_link = job.find('div', class_= '_3uiq0PN').find('a', class_= '_17sHMz8')

            
            #Get necessary data
            job_title = job_link.text
            advertiser_name = advertiser_link.text
            short_description = short_description_link.text
            job_location = job_location_link.text

            #Get url for the child
            child_link = self.base_url + job_link.get('href')

            #Input all data to parent_dict

            parent_dict['Job Ad Title'] = job_title
            parent_dict['Advertiser  Name'] = advertiser_name
            parent_dict['Short Description Text '] = short_description
            parent_dict['Job Ad location'] = job_location

            #Get child dict
            child_dict = self.parse_data_child(child_link)

            #Merge them together
            overall_dict = dict(parent_dict,**child_dict)
        
            #Append to parent result
            result.append(overall_dict)
            
        return result

    def concat_keyword(self,keyword):
        data = keyword.split()
        res_key = ""

        for val in data:
            if val == data[-1]:
                res_key += (val+'-jobs')
            else:
                res_key += (val+'-')
        
        return res_key

    def write_csv(self,):
        print('Saving to csv....')

        if self.result: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)
        print("Saved to results.xlsx")


    def run(self,):
        
        #Get keyword and pages
        keyword = input('Enter your keyword: ')
        pages = input('Enter number of pages to crawl: ')

        # try_link = 'https://www.seek.com.au/software-engineer-jobs?sortmode=ListedDate'

        # response = self.fetch(try_link)
        # test = self.parse_data_parent(response)

        # print(test)

        #Parsing keyword
        keyword_parsed = self.concat_keyword(keyword) 
        #Loop to all the pages

        for page in range(1, int(pages)+1):
            link = self.base_url + '/' + keyword_parsed + '?' + 'page=' + str(page) +'&sortmode=' + self.sort_mode
            
            #Fetching link
            response = self.fetch(link)
            parsed_result = self.parse_data_parent(response)

            self.result.extend(parsed_result)

        #Writing to csv
        self.write_csv()


if __name__ == '__main__':
    scraper = ScrapeSeek()
    scraper.run()