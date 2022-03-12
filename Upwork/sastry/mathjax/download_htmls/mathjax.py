from csv import excel_tab
from selenium import webdriver  
import time  
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from typing import List

from time import sleep

urls_list: List = []

with open("inputs.txt") as f:
    urls_list = [x.strip() for x in f.readlines()]

result: List = []

for url in urls_list[:10]:
    _feature: dict = {}
    # driver = webdriver.Chrome(r"C:\Users\USER\Downloads\chromedriver.exe")
    driver = webdriver.Firefox()
    driver.get(url)   

    web_string = driver.find_element(By.XPATH, '//*[@id="content"]')
    blocks = web_string.find_element(By.CSS_SELECTOR, "div.entry-content")
    sub_elemnets = blocks.find_elements_by_xpath("./*") 
    final_string: str = ''

    for elem in sub_elemnets:
        final_string += elem.text.strip().replace("\n", "") + "\n\n"
    
    final_string = final_string.strip()
    final_string = '\n'.join(final_string.split("\n")[:-1])

    _feature["url"] = url
    _feature["title"] = driver.title
    _feature["content"] = final_string

    result.append(_feature)

    driver.quit()

df = pd.DataFrame(result)

df.to_csv("result.csv")

print ("############################# ALL COMPLETED ####################################")