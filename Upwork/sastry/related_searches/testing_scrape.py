# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from urllib.parse import urljoin
import requests
import re
import json
import io 
from bs4 import BeautifulSoup

# API = '89f53273207f9aacdce3069e17dfceb0'     
# def get_url(url):
#     payload = {'api_key': API, 'url': url, 'country_code': 'fr'}
#     proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)

#     return proxy_url

# url = get_url("https://www.google.com/search?q=Kelston+Modular+Sofa+-+Case+Furniture+")

# response = requests.get(url)
    
# with io.open("new_test.html", 'w', encoding = 'utf-8') as html_file:
#     html_file.write(response.text)
# print('Done')


# username = "geonode_ZBIBKUHwEN-country-GB-autoReplace-True"
# username = "geonode_ZBIBKUHwEN-country-BR-autoReplace-True"
username = "geonode_ZBIBKUHwEN-country-GB-autoReplace-True"
password = "699adf28-70c8-4e73-8721-61de622713a9"
GEONODE_DNS = "premium-residential.geonode.com:9000"

# urlToGet = "http://www.google.co.uk/search?q='Valentine Tallboy - Case Furniture"
urlToGet = "http://www.google.co.uk/search?q='675 Chair - Case Furniture"
proxy = {"http":"http://{}:{}@{}".format(username, password, GEONODE_DNS)}
response = requests.get(urlToGet , proxies=proxy)

# with io.open("new_test.html", 'w', encoding = 'utf-8') as html_file:
#     html_file.write(response.text)

content = BeautifulSoup(response.content, 'lxml')
# all_divs = content.find_all("div", {"class": "BNeawe s3v9rd AP7Wnd lRVwie"})
all_divs = content.find_all("div", {"class": "gGQDvd iIWm4b"})

if all_divs:
    for div in all_divs:
        print(div.text)

