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


class VotivaProvider():
    
    def __init__(self):
        self.base_url = 'https://inmodemd.com/physician-finder/'
        self.driver = webdriver.Firefox()

        self.result: List[dict] = []

        self.processed_facility = set()

        #For storing parsed zip codes
        self.parsed_zip: List[dict] = []
        self.saved_to_parsed: List[dict] = []

        #For storing and getting results
        self._results_old: List[dict] = []
        self._results_new: List[dict] = []
        self._processed_results = set()

        #Url for zip codes
        self.url_zip = 'https://informationngr.com/us-zip-codes-list/'
        self.zip_code_list: List[int] = []

        #Search parameters
        self.technology = 15651 #votiva

        #Go to base url
        self.driver.get(self.base_url)

    def _search(self,zip_code):

        print("searching businesses within zip code:", zip_code)

        #Accept and close
        try:
            accept_close = self.driver.find_element_by_class_name('saveclose')
            accept_close.click()
        except:
            pass
        #Zip code
        zip_elem = self.driver.find_element_by_id('location')
        zip_elem.send_keys(zip_code)

        #Technology
        tech_elem = Select(self.driver.find_element_by_id('treatment'))
        tech_elem.select_by_visible_text('Votiva')

        submit = self.driver.find_element_by_name('submit')
        submit.click()


    def _parse_data(self,):

        try:
            _data = self.driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div/main/section[3]/div/div/div/div/div')

            for data in _data:
                data_dict = {}
                
                try:
                    data_dict['Business Name'] = data.find_element_by_class_name('dr-name').text.strip()
                except:
                    data_dict['Business Name'] = ''
                try:
                    data_dict['Doctor/Owner/CEO'] = data.find_element_by_class_name('dr-subname').text.strip()
                except:
                    data_dict['Doctor/Owner/CEO'] = ''
                try:
                    data_dict['Business Website'] = ' '.join(data.find_element_by_class_name('dr-website').text.strip().split(' ')[1:])
                except:
                    data_dict['Business Website'] = ''
                try:
                    data_dict['Business Address'] = ' '.join(data.find_element_by_class_name('dr-address').text.strip().split(' ')[1:])
                except:
                    data_dict['Business Address'] = ''
                try:
                    data_dict['Business Phone'] = ' '.join(data.find_element_by_class_name('dr-phone').text.strip().split(' ')[1:])

                except:
                    data_dict['Business Phone'] = ''

                if not data_dict['Business Name'] in self.processed_facility:
                    self.result.append(data_dict)
                    self.processed_facility.add(data_dict['Business Name'])
                else:
                    continue

            # self.driver.execute_script("window.history.go(-1)")
            self.driver.back()
        except:
            pass



    def _get_zip_code(self,):

        req_zip = requests.get(self.url_zip)

        content = BeautifulSoup(req_zip.text, 'lxml')


        zip_codes = content.find('figure', class_ = 'wp-block-table is-style-stripes')

        _zip_codes = zip_codes.find_all('tr')[1:]

        for zip_code in _zip_codes:
            zip = zip_code.find_all('td')[-1].text
            try:
                self.zip_code_list.append(int(zip))
            except:
                self._extend_zip(zip)

    def _extend_zip(self, zip_str: str):

        nums = re.findall(r'\d+', zip_str)

        if nums == ['49036','49734','49735']:
            new_nums = [['49036'],['49734','49735']]
        else:
            new_nums = self._split(nums,2)

        for pairs in new_nums:
            if len(pairs) == 2:
                self._start_to_end(pairs)
            else:
                self.zip_code_list.append(int(pairs[-1]))

    def _start_to_end(self, pairs):
        for x in range(int(pairs[0]), (int(pairs[-1])+1)):
            self.zip_code_list.append(int(x))

    def _split(self,arr, size):
        '''Splits list.'''
        arrs = []
        while len(arr) > size:
            pice = arr[:size]
            arrs.append(pice)
            arr   = arr[size:]
        arrs.append(arr)
        return arrs

    def _run(self,):
        

        self._load_csv()
        self._load_data()

        self._get_zip_code()
        # test_list: List[int] = [94027,11962,90402,90210,98039,33109,2176,4106,75001,77001]

        try:
            for code in self.zip_code_list:
                if code in [int(x['parsed']) for x in self.parsed_zip]:
                    print('zip code <{}> is already parsed'.format(code))
                    continue
            # for code in test_list:
                #trying with one zip code
                else:
                    try:
                        time.sleep(1)
                        self._search(str(code))
                        # time.sleep(1)
                        self._parse_data()
                        self.saved_to_parsed.append({'parsed': code})
                    except Exception:
                        continue
        except KeyboardInterrupt:
            pass
        finally:
            try:
                self.saved_to_parsed = self.saved_to_parsed + self.parsed_zip
                self._clean_data()
            except:
                None

            self._save_parsed()
            self.write_csv()

    def _clean_data(self,):
        try:
            for value in (self._results_old + self.result):
                if value['Business Name'] in self._processed_results:
                    continue
                else:
                    self._results_new.append(value)
                    self._processed_results.add(value['Business Name'])
            self._results_new = list(set(self._results_new))
        except:
            raise Exception


    def _save_parsed(self,):

        print('saving parsed data')

        if self.saved_to_parsed: 
            with open('parsed.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.saved_to_parsed[0].keys())
                writer_object.writeheader()

                for row in self.saved_to_parsed:
                    writer_object.writerow(row)
            print("parsed zip codes saved to parsed.csv")
        
        else:
            print('no data was saved to parsed.csv')

    def _load_csv(self,):

        print('opening parsed.csv')
        try:
            with open('parsed.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.parsed_zip.append(row)
        except Exception as e:
            print(e)
            pass

    def _load_data(self,):

        print('opening results.csv')
        try:
            with open('results.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self._results_old.append(row)
        except Exception as e:
            print(e)
            pass


    def write_csv(self,):
        '''Save results to csv.'''
        print('saving to csv....')

        if self._results_new: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self._results_new[0].keys())
                writer_object.writeheader()

                for row in self._results_new:
                    writer_object.writerow(row)
            print("saved to results.csv")
        
        else:
            print('no data was saved')

if __name__ == '__main__':

    scrape = VotivaProvider()
    scrape._run()

    # scrape._run()