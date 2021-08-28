import re
import requests
import pandas as pd
import time 
import time 
import csv

from collections import deque
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from typing import List
from bs4 import BeautifulSoup


class InstagramScraper:

    def __init__(self) -> None:
        '''Initialize variables used for scraping.'''
        self.base_url = 'https://www.google.com/search?q=site:instagram.com+%22miami%22+-estate+-realtor+-food+AND+'
        self.driver = webdriver.Firefox()

        #Credentials
        USERNAME = 'rexvon.apaap@gmail.com'
        PASSWORD = 'bryitkids920'

        # self.unprocessed_urls = deque([])
        self.processed_urls: List[str] = []

        self.result: List[dict] = []

        self.driver.get(self.base_url)

    def __login_(self)->None:

        driver = webdriver.Firefox()

        _login_url = 'https://www.instagram.com/accounts/login/'
        driver.get(_login_url)

        _user = driver.find_elements_by_class_name('_2hvTZ pexuQ zyHYP')[0]
        _user.send_keys(self.USERNAME)

        _password = driver.find_elements_by_class_name('_2hvTZ pexuQ zyHYP')[-1]
        _password.send_keys(self.PASSWORD)

        _button = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button')
        _button.click()

        time.sleep(3)
        driver.close()
        pass

    def _search(self, page):
        '''Fetch the url and returns bs4 object.'''
        self.pagination_params['start'] = str(10*page)
        self.pagination_params['q'] = self.keyword
        self.pagination_params['oq'] = self.keyword

        response = requests.get(self.base_url, params = self.pagination_params, headers = self.headers)

        return response


    def _get_urls(self,):
        '''Parse the urls contained in the page and append to results.'''

        #Get the content of results page
        div_rso = self.driver.find_element_by_id('rso')

        div_class_g = div_rso.find_elements_by_class_name('g')

        for div in div_class_g:

            link = div.find_element_by_tag_name('a')
            url = link.get_attribute('href')
    
            # if not url in self.unprocessed_urls and not url in self.processed_urls:
            if not url in self.processed_urls:
                print(url)
                self.processed_urls.append(url)
                self._profilescraper(url)


    def _profilescraper(self, url):

        driver = webdriver.Firefox()
        driver.get(url)

        # try:
        #     _prof_link = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/a')
        #     _prof_link.click()
        #     time.sleep(1)

        # except:
        #     pass




        time.sleep(3)

        driver.close()

        # print(_section.prettify())



    def write_csv(self,):
        '''Save results to csv.'''
        print('Saving to csv....')

        if self.result: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)
            print("Saved to results.xlsx")
        
        else:
            print('No data was saved')
            

    def store_response(self, response, page):
        '''Saved response as html.'''
        if response.status_code == 200:
            print('Saving response as html')
            filename = 'res' + str(page) + '.html'
            with io.open(filename, 'w', encoding = 'utf-8') as html_file:
                html_file.write(response.text)
            print('Done')
        else:
            print('Bad response!')
  
    def load_response(self,):
        '''Load an html file.'''
        html = ''
        with open('res.html', 'r') as html_file:
            for line in html_file.read():
                html += line
        return html
        
    def run(self,):
        '''Run all cases using the keyword'''

        self.__login_()

        while(True):
            self._get_urls()
            break
        # for page in range(1,(int(self.pages)+1)):
        #     resp = self.fetch(page-1)
        #     # self.store_response(resp,page)
        #     self.parse(resp.content)
        # self.write_csv()

if __name__ == '__main__':

    # keyword = input('Enter your keyword: ')
    # pages = input('Number of pages: ')
    keyword = 'site:instagram.com "miami" -estate -realtor -food AND'
    pages = 1
    #Run scraper
    scraper = InstagramScraper()
    scraper.run()
