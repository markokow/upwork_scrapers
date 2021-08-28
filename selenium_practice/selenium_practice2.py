from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time 

driver = webdriver.Firefox()
URL = 'https://crs.upd.edu.ph/'

driver.get(URL)
search = driver.find_element_by_name('txt_login')
search.send_keys('raapaap')
search = driver.find_element_by_name('pwd_password')
search.send_keys('bryitkids')

login = driver.find_element_by_xpath("//input[@value='Login']")
print(login) 

login.click()

