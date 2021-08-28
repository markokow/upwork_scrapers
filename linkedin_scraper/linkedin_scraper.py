from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time 


class LinkedInScraper():
    def __init__(self,):
        self.base_url = 'http://www.linkedin.com/uas/login'

        #Initalize
        self.driver = webdriver.Firefox()

        #Wait


        #Credentials
        self.email = 'rex.von.brixon.apa-ap@eee.upd.edu.ph'
        self.password = 'bryitkids'

    def _explicitwait(self,):

        try:
            home = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'identity-headline t-12 t-black--light t-normal mt1')))
            
            print(home.text)

        except Exception as e:
            print(e)
        # print(home.text)

    def _login(self,):
        '''Login to linkedin'''

        self.driver.get(self.base_url)
        
        _user = self.driver.find_element_by_id('username')
        _user.send_keys(self.email)

        _pass = self.driver.find_element_by_id('password')
        _pass.send_keys(self.password)
        
        _pass.submit()

    def _run(self,):

        self._login()
        self._explicitwait()






if __name__ == '__main__':

    scrape = LinkedInScraper()

    scrape._run()