import time 
import time 
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FreeImages():

    def __init__(self):

        self.driver = webdriver.Firefox()

        self.base_url = 'https://www.dreamstime.com/photos-images/'

        self.processed: List[str] = []
        self.result: List[dict] = []
        self.inputs: List[dict] = []


    def fetch(self, link, count = 0):
        count+=1
        if count == 2:
            return None
        try:
            self.driver.get(link)
            _src = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/div[2]/div/div/div[1]/a/img'))).get_attribute("src")
            time.sleep(1)
       
            return _src
        except:
            self.driver.quit()
            self.driver = webdriver.Firefox()
            self.fetch(link, count=count)



    def _parse(self,):

        for _val in self.result:
            print(_val['name'], 'already in result.csv')
            self.processed.append(_val['name'])

        for _input in self.inputs:
            _name = _input['name']

            if _name in self.processed:
                
                continue
            else:
                _stripped = _name.replace(' ','-') + '-white'

                try:
                    _url = self.base_url + _stripped
                    _src = self.fetch(_url)

                    _input['source'] = _src

                    print(_src)

                    if _src is not None:
                        self.result.append(_input)
                    else:
                        continue
                except Exception as e:
                    print(e)
                    continue




    def load_input(self,):
        try:
            with open('inputs.csv', 'r', newline = '',encoding = 'utf-8') as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:

                    self.inputs.append(row)
        except:
            print('CSV does not exit')

    def load_result(self,):
        try:
            with open('results.csv', 'r', newline = '',encoding = 'utf-8') as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:

                    self.result.append(row)
        except:
            print('CSV does not exit')




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

        try:
            self.load_input()
            self.load_result()
            self._parse()
        except KeyboardInterrupt:
            pass
        self.write_csv()
        # print(self.inputs)

        # _resp = self.fetch(self.base_url)
        # self._parse(_resp)
        # self.write_csv()


if __name__ == '__main__':
    # try_link = 'https://www.organics.ph/'
    # try_link = 'https://www.vq.org.au/play-learn/find-club/?postcode'

    scraper = FreeImages()

    scraper.run()