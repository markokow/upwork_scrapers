import re
from types import CodeType
import requests
import pandas as pd
import time 
import time 
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from typing import List
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class gia_report():
    
    def __init__(self):
        self.driver = webdriver.Firefox()

        self._target_url: List[str] = []
        self.result: List[dict] = []

    def _search(self, url):

        _dict_data: dict = {}

        self.driver.get(url)

        print("searching url", url)

        #Accept and close
        try:

            while(True):

                _src = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="multimediaPDFPopUpId"]'))).get_attribute("src")

                if(bool(_src)):
                    break
                else:
                    continue

            _dict_data['URL'] = url
            _dict_data['GIA Number'] = _src.split('/')[-1].replace('.pdf','')

            print(_dict_data)
            self.result.append(_dict_data)


        except Exception as e:
            print(e)

    def _load_csv(self,):

        print('opening target.csv')
        try:
            with open('target.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self._target_url.append(row[0])
        except Exception as e:
            print(e)
            pass


    def write_csv(self,):
        '''Save results to csv.'''
        print('saving to csv....')


        if self.result: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)
            print("saved to results.csv")
        
        else:
            print('no data was saved')
            
                
    def _run(self,):
        
        self._load_csv()

        for _url in self._target_url:
            self._search(_url)
            # break

        self.write_csv()

if __name__ == '__main__':

    scrape = gia_report()
    scrape._run()

    # scrape._run()