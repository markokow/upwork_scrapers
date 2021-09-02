from selenium import webdriver
from typing import List

from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *



class _classAmazon():
    
    def __init__(self, _url_list: List[str] = []):
        self.url_list: List[str] = _url_list

        #Proxy
        self.myProxy = "157.245.222.183:80"

        self.proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': self.myProxy,
        'ftpProxy': self.myProxy,
        'sslProxy': self.myProxy,
        'noProxy':''})

        self.driver = webdriver.Firefox(proxy = self.proxy)

        self._result: List[dict] = []


    def _search(self, _url: str):

        self.driver.get(_url)
        #Accept and close
        try:
            _child_dict: dict = {}
            while(True):
                try:
                    _title = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'productTitle')))
                except:
                    _title = ''
                try:
                    _price = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'price_inside_buybox')))
                except:
                    _price = ''
                try:
                    _availability = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'availability')))
                except:
                    _availability = ''
                

                if (bool(_title)):
                    break


            _child_dict['Product Title'] = _title.text
            _child_dict['Price'] = _price.text
            _child_dict['Availability'] = _availability.text

            print(_child_dict)

            return _child_dict

        except:
            pass

    def _innerparse(self, _url: str = ''):
        '''Get content in amazon'''
        try:
            _child_dict = self._search(_url)
            if _child_dict:
                self._result.append(_child_dict)
            else:
                pass
        except:
            pass

    def _run(self,):
        '''Run the browser.'''
        for _url in self.url_list:
            self._innerparse(_url)
    
        self.driver.quit()
        
        return self._result


if __name__ == '__main__':

    scrape = _classAmazon()
    scrape._run()

    # scrape._run()