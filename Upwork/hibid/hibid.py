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
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.proxy import *
from pyvirtualdisplay import Display
# from xvfbwrapper import Xvfb

import requests
import requests.exceptions
import csv

from bs4 import BeautifulSoup
from typing import List



class Hibid():

    def __init__(self):

        # self.driver = webdriver.Firefox()

        self.base_url = 'https://www.google.com/maps/search/massage+in+united+states'
        self.driver = webdriver.Firefox()


        self.processed: List[str] = []
        self.result: List[dict] = []


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

    def _fetch(self, link):
        try:
            response = requests.get(link)
        except:
            raise Exception

        return response


    def spider_url_firefox_by_whiteip(self,url):
        browser = None
        display = None
        
        ##  white list ip, please see the mipu agent member center ： https://proxy.mimvp.com/usercenter/userinfo.php?p=whiteip
        mimvp_proxy = { 
                        'ip'            : '140.143.62.84',      # ip
                        'port_https'    : 19480,                # http, https
                        'port_socks'    : 19481,                # socks5
                        'username'      : 'mimvp-user',
                        'password'      : 'mimvp-pass'
                    }
        
        try:
            # display = Display(visible=0, size=(800, 600))
            # display.start()
            
            profile = webdriver.FirefoxProfile()
            
            # add proxy
            profile.set_preference('network.proxy.type', 1)     # ProxyType.MANUAL = 1
            if url.startswith("http://"):
                profile.set_preference('network.proxy.http', mimvp_proxy['ip'])
                profile.set_preference('network.proxy.http_port', mimvp_proxy['port_https'])    #  visit http sites 
            elif url.startswith("https://"):
                profile.set_preference('network.proxy.ssl', mimvp_proxy['ip'])
                profile.set_preference('network.proxy.ssl_port', mimvp_proxy['port_https'])     #  visit https sites 
            else:
                profile.set_preference('network.proxy.socks', mimvp_proxy['ip'])
                profile.set_preference('network.proxy.socks_port', mimvp_proxy['port_socks'])
                profile.set_preference('network.proxy.ftp', mimvp_proxy['ip'])
                profile.set_preference('network.proxy.ftp_port', mimvp_proxy['port_https'])
                profile.set_preference('network.proxy.no_proxies_on', 'localhost,127.0.0.1')
            
            ##  this usage does not exist. you cannot set your username and password this way  （ give up ）
    #         profile.set_preference("network.proxy.username", 'mimvp-user')
    #         profile.set_preference("network.proxy.password", 'mimvp-pass')
        
            profile.update_preferences()
            
            browser = webdriver.Firefox(profile)       #  open the FireFox  the browser 
            browser.get(url)     
            content = browser.page_source
            print("content: " + str(content))
        finally:
            if browser: browser.quit()
            if display: display.stop()



    def _parse(self,):


        # _tableid = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'companySearch_wrapper')))
        self.driver.find_element(By.XPATH("/html/body")).sendKeys(Keys.CONTROL, Keys.END);

        # print(_tableid)



        # for _val in self.result:
        #     print(_val['name'], 'already in result.csv')
        #     self.processed.append(_val['name'])

        # for _input in self.inputs:
        #     _name = _input['name']

        #     if _name in self.processed:
                
        #         continue
        #     else:
        #         _stripped = _name.replace(' ','-') + '-white'

        #         try:
        #             _url = self.base_url + _stripped
        #             _src = self.fetch(_url)

        #             _input['source'] = _src

        #             print(_src)

        #             if _src is not None:
        #                 self.result.append(_input)
        #             else:
        #                 continue
        #         except Exception as e:
        #             print(e)
        #             continue




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
            # resp = self._fetch(self.base_url)

            # print(resp.status_code)
            self.driver.get(self.base_url)
            self._parse()
            # self.spider_url_firefox_by_whiteip(self.base_url)
        except KeyboardInterrupt:
            pass
            # pass
        # self.write_csv()
        # print(self.inputs)

        # _resp = self.fetch(self.base_url)
        # self._parse(_resp)
        # self.write_csv()


if __name__ == '__main__':

    scraper = Hibid()

    scraper.run()