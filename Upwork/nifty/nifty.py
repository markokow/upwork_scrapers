import time 
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from typing import List

from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By



class _classNifty():
    
    def __init__(self):
        self.base_url = 'https://www.loudersound.com/features/the-best-budget-wireless-headphones'
        self.driver = webdriver.Firefox()
        # self.driver= webdriver.Chrome(executable_path='put path here})

        self.result: List[dict] = []

        #Go to base url

        self.index = 'NIFTY 50'
        self.start_date = '01-08-2021'
        self.end_date = '30-08-2021'

    def _search(self):

        print("searching url", self.base_url)


        #Accept and close
        try:
            self.driver.get(self.base_url)

            tech_elem = Select(self.driver.find_element_by_id('indexType'))
            tech_elem.select_by_visible_text(self.index)

            _start_date = self.driver.find_element_by_id('fromDate')
            _start_date.send_keys(self.start_date)

            _end_date = self.driver.find_element_by_id('toDate')
            _end_date.send_keys(self.end_date)

            _get_data = self.driver.find_element_by_id('get')
            _get_data.click()


        except Exception as e:
            print(e)

    def _parse_data(self):

            attemps: int = 10

            while(True):
                _data = self.driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[2]/div[1]/div[4]/div/div[2]/table/tbody/tr')
                if (bool(_data) or (not attemps)):
                    if not attemps:
                        print('No data count after 10 attemps')
                    break
                else:
                    self.driver.quit()
                    self.driver = webdriver.Firefox()
                    self._search()
                    attemps-=1
                    continue

            for dat in _data[3:-1]:
                
                _values = dat.text.split()

                _dict_data: dict = {}
                
                _dict_data['Date'] = _values[0]
                _dict_data['Open'] = _values[1]
                _dict_data['High'] = _values[2]
                _dict_data['Low'] = _values[3]
                _dict_data['Shares Traded'] = _values[4]
                _dict_data['Turnover(₹Cr)'] = _values[5]

                self.result.append(_dict_data)

    def write_csv(self,):
        '''Save results to csv.'''
        print('saving to csv....')

        _from = self.start_date.replace('-','')
        _to = self.end_date.replace('-','')

        _filename = '{}-{}-{}.csv'.format(self.index.replace(' ',''),_from,_to)

        if self.result: 
            with open(_filename, 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)
            print("saved to {}".format(_filename))
        
        else:
            print('no data was saved')
                
    def _run(self,):
        
        self._search()
        # self._parse_data()
        # self.write_csv()

if __name__ == '__main__':

    scrape = _classNifty()
    scrape._run()

    # scrape._run()