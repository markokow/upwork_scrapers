# Adapted from example in Ch.3 of "Web Scraping With Python, Second Edition" by Ryan Mitchell

import re
import requests
from bs4 import BeautifulSoup
import csv

pages = set()
results = []

def get_links(page_url):
    global pages
    #   pattern = re.compile("^(/)")
    _headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    }

    proxy = {
        # 'https': 'https://41.217.219.53:31398'
    }
    html = requests.get(page_url, headers=_headers, proxies=proxy) # fstrings require Python 3.6+
    

    print(html.status_code)

    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a", href=True):

        dict_data: dict ={}

        if link["href"] not in pages and link['href'].startswith('/'):
            new_page = page_url[:-1] + link["href"]
            # print(new_page)
            pages.add(new_page)

            dict_data['Link text'] = link.text
            dict_data['URLs'] = new_page

            print(dict_data)

            results.append(dict_data)

            if new_page.startswith(page_url) and new_page != page_url:
                get_links(new_page)
            else:
                continue

def write_csv():
        print('Saving to csv....')

        if results: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = results[0].keys())
                writer_object.writeheader()

                for row in results:
                    writer_object.writerow(row)
        print("Saved to results.xlsx")



get_links('https://www.sustainablesupply.com/')
write_csv()
        