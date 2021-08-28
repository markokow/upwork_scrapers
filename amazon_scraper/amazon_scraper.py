import csv
from bs4 import BeautifulSoup

from selenium import webdriver


#Startup the webdriver
driver = webdriver.Firefox()

URL = 'https://www.amazon.com/'
# driver.get(URL)

def get_url(search_term):
    '''Generate URL.'''
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss'
    search_term = search_term.replace(' ', '+')

    return template.format(search_term)

print(get_url('wazzup'))


