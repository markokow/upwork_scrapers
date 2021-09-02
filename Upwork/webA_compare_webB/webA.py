import re
import requests
import pandas as pd
import time 
import time 
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from typing import List
from bs4 import BeautifulSoup


class WebA():
    
    def __init__(self):
        self.base_url = 'https://www.mouser.com/Semiconductors/Integrated-Circuits-ICs/Driver-ICs/_/N-7zhz5Z1yzvvqx'
        self.driver = webdriver.Firefox()

        self.result: List[dict] = []

        # self.processed_facility = set()

        #Go to base url
        self.driver.get(self.base_url)

    def _go_next(self):

        try:
            _nationality = self.driver.find_element_by_id('1_divRightFlagImg')
            _nationality.click()
        except:
            pass
        #Accept and close
        try:
            _next = self.driver.find_element_by_id('lnkPager_lnkNext')
            _next.click()
        except:
            pass


    def _parse_data(self,):


        _data = self.driver.find_elements_by_xpath('/html/body/main/div/div/div[1]/div[6]/div/form/div[2]/div[2]/table/tbody/tr')

        for data in _data:
            data_dict = {}
            
            try:
                data_dict['Mrf. Part #'] = data.find_element_by_class_name('part-number-lbl')[0].text.strip()
            except:
                data_dict['Mrf. Part #'] = ''

            try:
                data_dict['Mouser Part #'] = data.find_element_by_class_name('part-number-lbl')[-1].text.strip()
            except:
                data_dict['Mouser Part #'] = ''

            # try:
            #     data_dict['Mfr.'] = ' '.join(data.find_element_by_class_name('dr-website').text.strip().split(' ')[1:])
            # except:
            #     data_dict['Mfr.'] = ''

            # try:
            #     data_dict['Description'] = ' '.join(data.find_element_by_class_name('dr-address').text.strip().split(' ')[1:])
            # except:
            #     data_dict['Description'] = ''

            # try:
            #     data_dict['Quantity'] = ' '.join(data.find_element_by_class_name('dr-phone').text.strip().split(' ')[1:])

            # except:
            #     data_dict['Quantity'] = ''

            # try:
            #     data_dict['Status'] = ' '.join(data.find_element_by_class_name('dr-phone').text.strip().split(' ')[1:])

            # except:
            #     data_dict['Status'] = ''

            # if not data_dict['Business Name'] in self.processed_facility:
            self.result.append(data_dict)
            #     self.processed_facility.add(data_dict['Business Name'])
            # else:
            #     continue

        # self.driver.execute_script("window.history.go(-1)")
        self.driver.back()

    def _run(self,):

        max_count = 3

        for i in range(1,max_count):
            print('searching page:',i)
            self._parse_data()
            time.sleep(2)
            self._go_next()
            time.sleep(2)

        print(self.result)


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

if __name__ == '__main__':

    scrape = WebA()
    scrape._run()

    # scrape._run()