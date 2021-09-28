import csv
import requests
from bs4 import BeautifulSoup
import io
from datetime import datetime
from urllib.request import urlopen, Request
from typing import Any, Union, List
import re

class GoogleScraper:

    def __init__(self, keyword = 'google', pages = 1) -> None:
        '''Initialize variables used for scraping.'''
        self.keyword: str = keyword
        self.pages: int = pages
        self.base_url: str = 'https://www.google.com/search'
        self.keyword_list: List = []
        self.result: List = []

        self.pagination_params = {
            'q':'query',
            'biw':'1858',
            'bih':'668',
            'ei':'LGAhYYDqIJrr-QbwprHwCw',
            'oq':'rex',
            'gs_lcp':'Cgdnd3Mtd2l6EAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAELADEEMyCgguEMgDELADEEMyCgguEMgDELADEEMyCgguEMgDELADEEMyCgguEMgDELADEENKBQg4EgExSgQIQRgAUABYAGCNog5oAXACeACAAZ8FiAGfBZIBAzUtMZgBAMgBDcABAQ',
            'sclient':'gws-wiz',
            'ved':'0ahUKEwiAsP6t-MLyAhWadd4KHXBTDL4Q4dUDCA0',
            'start': '0',
            'uact':'5',
        }

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Alt-Used': 'www.google.com',
            'Connection': 'keep-alive',
            'Cookie': 'CGIC=CgtmaXJlZm94LWItZCJKdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2Uvd2VicCwqLyo7cT0wLjg; NID=221=wL8YmOu0tOO1VTGJ6A_4UVAroscl7GjzDMgjsLa6BHPtqFx-3By-Q9IpfxE6_15UUCegybfa46UPQTa681lb_Lu3m_MbqQ96Y4UwxI2xpELsg9y0BKLfCtcejzVhKHncHe0XM966akkMkMemzdlT3F_tIhtSLvNkjx1LHn3pYToZILT41wkYLs2zjLcM3b8IjoiWvYzfXBnGxKTxjHr-z46dj9-YjsOB61xs-syp-SXgMJEPLrxrHwK5vjzheEo1iRP_ydovs9rMgw70713iEN_vAYOR2b-UV6v2aq2WhETODBdF22g5yxWpUozlqLMzNJXk4RNZThD0jm7DxGQv3Rc53MHE_TQBXm0GVjerivgjOUErecVXU5b26uOpbvWVo41t69mWB8_QfPpwF01yROJLy1SVJbQhTA7PxWk7fVcozO8Y0eOtn3eFtX6R_gzlhMhDFr9P1aBIAnkSWMVRfBosYvLZp9ASpXllNJwMN5uOlDwryjigVBYivrlHUMVl8olmkPnmav3Q; 1P_JAR=2021-08-21-21; ANID=AHWqTUmTm5iBdRbl0pirNTP0WWU64d9o6iblGeKMLj23NMVIX8r3-g0lNVgQ6QdW; SID=BAioqx10FUJklsDbHGI1tjiY4xxczIvQHGIreeKx-2xwsIO3dTRFo9kkT-n-yOhnex5axw.; __Secure-3PSID=BAioqx10FUJklsDbHGI1tjiY4xxczIvQHGIreeKx-2xwsIO3yn44exF-jV2qGrJRtX0f3w.; HSID=ARJWQjooC9F3Qri8t; SSID=AH0aXRmd6fp_WDBT1; APISID=kl7LxO9PiLHYMkIR/AWFV7CwwM3pk-xGIJ; SAPISID=i4JG_BZH2WbZf7e-/A_SlHYeSkZspWm0Ny; __Secure-3PAPISID=i4JG_BZH2WbZf7e-/A_SlHYeSkZspWm0Ny; SIDCC=AJi4QfEt8yMasAGQY1K_dTunCIfXnlw3DAee8BmN9pNtiNWcNVuapKDioXyRgKCgIxYZ1uR_zYOr; SEARCH_SAMESITE=CgQI7ZIB; __Secure-1PSID=BAioqx10FUJklsDbHGI1tjiY4xxczIvQHGIreeKx-2xwsIO3o3qiwieENH072zKs3UYiYQ.; __Secure-1PAPISID=i4JG_BZH2WbZf7e-/A_SlHYeSkZspWm0Ny; __Secure-3PSIDCC=AJi4QfEFsGAQC-x6xsEfZTXPE5mTUMBrfrrtiPTlShj-KAakcynF7OSgX8MJDyjWjHXMtynv90xs; OTZ=6109530_24_24__24_; DV=01_uKYrXMkweYPXf0FOdhZDXDUyqthc',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers',
        }

    def fetch(self, page):
        '''Fetch the url and returns bs4 object.'''
        self.pagination_params['start'] = str(10*page)
        self.pagination_params['q'] = self.keyword
        self.pagination_params['oq'] = self.keyword

        response = requests.get(self.base_url, params = self.pagination_params, headers = self.headers)
        # response = requests.get(self.base_url, params = self.pagination_params, headers = self.headers)

        return response

    def parse(self, html):
        '''Parse the urls contained in the page and append to results.'''
        content = BeautifulSoup(html, 'lxml')

        #Get the content of results page
        div_rso = content.find('div', {'id': 'rso'})

        div_class_g = div_rso.find_all('div', class_ = 'g')

        for div in div_class_g:
            url = div.find('a', href = True)['href']

            print('scraping...',url)
            self.result.append(
                {
                    'URL/s': url
            })

    def write_csv(self,):
        '''Save results to csv.'''
        print('Saving to csv....')

        if self.result: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)

        print("Saved to results.xlsx")
        
    def store_response(self, response, page):
        '''Saved response as html.'''
        if response.status_code == 200:
            print('Saving response as html')
            filename = 'res' + str(page) + '.html'
            with io.open(filename, 'w', encoding = 'utf-8') as html_file:
                html_file.write(response.text)
            print('Done')
        else:
            print('Bad response!')
  
    def load_response(self,):
        '''Load an html file.'''
        html = ''
        with open('res.html', 'r') as html_file:
            for line in html_file.read():
                html += line
        return html
        

    def run(self,):
        '''Run all cases using the keyword'''
        self.keyword_list = [x.lower() for x in self.keyword.split()]

        #Run all pages
        for page in range(1,int(self.pages)+1):
            resp = self.fetch(page-1)
            # self.store_response(resp,page)
            self.parse(resp.content)

        self.write_csv()

if __name__ == '__main__':

    # keyword = input('Enter your keyword: ')
    # pages = input('Number of pages: ')
    keyword = 'hey'
    pages = 1000
    #Run scraper
    scraper = GoogleScraper(keyword, pages)
    scraper.run()
