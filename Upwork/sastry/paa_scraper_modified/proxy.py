import requests
from bs4 import BeautifulSoup
import json
import io

# payload = {'api_key': '89f53273207f9aacdce3069e17dfceb0', 'url':'https://httpbin.org/ip', 'render': 'true', 'country_code': 'us'}
# r = requests.get('http://api.scraperapi.com', params=payload)
# content = BeautifulSoup(r.content, 'lxml')
# _ip = eval(content.text)["origin"]
# print(_ip)
# Scrapy users can simply replace the urls in their start_urls and parse function
# ...other scrapy setup code
# start_urls = ['http://api.scraperapi.com?api_key=APIKEY&url=' + url +'&render=true' + ‘&country_code=true’]
# def parse(self, response):
#   # ...your parsing logic here
#   yield scrapy.Request('http://api.scraperapi.com/?api_key=APIKEY&url=' + url +'&render=true' + ‘&country_code=true’, parse)

proxyDict = { 
        "https" : '', 
    }

# proxyDict['https'] = f"https://{str(_ip)}:8080"


headers = {
        'User-Agent': 'Mozilla/5.0',
    }

# response = requests.get(f"https://www.google.com/search?q=testing", headers = headers, proxies=proxyDict)
response = requests.get(f"http://api.scraperapi.com?api_key=89f53273207f9aacdce3069e17dfceb0&url=https://www.google.com/search?q=testing", headers = headers)

with io.open("Testt.html", 'w', encoding = 'utf-8') as html_file:
    html_file.write(response.text)