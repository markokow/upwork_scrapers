import csv
import requests
from bs4 import BeautifulSoup
import io
from datetime import datetime
from urllib.request import urlopen, Request
from typing import Any, Union, List
import time
import winsound
from urllib.parse import urlparse

from requests.models import cookiejar_from_dict

class GoogleScraper:

    def __init__(self, keyword = 'google', pages = 1, cookies = '') -> None:
        '''Initialize variables used for scraping.'''
        self.keyword: str = keyword
        self.pages: int = pages
        self.base_url: str = 'https://www.google.com/search'
        self.keyword_list: List = []
        self.result: List = []
        self._taken: List = []
        self._done: List = []
        self._counter: int = 0

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
            'Cookie': cookies,

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

    def _check_url(self, _url:str = ''):

        _res = requests.get(_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'})

        if _res.status_code == 200:

            if 'scripts.mediavine.com' in _res.text:

                _main_url = urlparse(_url).netloc

                if _main_url in self._done:
                    print("already parsed:",_main_url)
                else:
                    print("valid url:", _main_url)

                    _soup = BeautifulSoup(_res.text, 'html.parser')

                    _valid_url = {
                        'valid_urls': _main_url,
                        'title': _soup.title.text,
                        'meta': _soup.meta
                    }

                    self._done.append(_main_url)
                    self._counter+=1
                    self.result.append(_valid_url)

    def parse(self, html):
        '''Parse the urls contained in the page and append to results.'''
        content = BeautifulSoup(html, 'lxml')

        #Get the content of results page
        div_rso = content.find('div', {'id': 'rso'})

        div_class_g = div_rso.find_all('div', class_ = 'g')

        for div in div_class_g:
            url = div.find('a', href = True)['href']

            _main_url = urlparse(url).netloc

            if _main_url in self._done:
                print("already parsed:",_main_url)
            else:
                if not _main_url.startswith('http'):
                    _main_url = 'http://' + _main_url
                try:
                    self._check_url(_url = _main_url)
                except:
                    continue


            # print('scraping...',url)
            # self.result.append(
            #     {
            #         'URL/s': url
            # })

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
    
    def open_csv(self):

        print("opening csv")
        with open('results.csv', 'r', newline = '', encoding= 'utf-8') as csv_file:
            _dict_reader = csv.DictReader(csv_file)
            self._taken = list(_dict_reader)
        

        self._done = [_val['valid_urls'] for _val in self._taken]

        self.result = self._taken

        print(self.result)


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
        self.open_csv()

        #Run all pages
        for page in range(1 ,int(self.pages)+1):
            print("current page:", page)
            try:
                try:
                    resp = self.fetch(page-1)
                    # self.store_response(resp,page)
                    self.parse(resp.content)
                    time.sleep(1)
                except KeyboardInterrupt:
                    break
            except Exception as e:
                print(e)
                break
        self.write_csv()
        print(self._counter, "urls added to result.csv")
        winsound.Beep(440,3000)

if __name__ == '__main__':

    keyword = 'God site mediavine'
    pages = 1000000
    cookies = ''
    cookies = 'CGIC=CgtmaXJlZm94LWItZCJKdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2Uvd2VicCwqLyo7cT0wLjg; NID=511=a2vaw6MG2kia-n3yRUpyhX2Qz6mMo4wnJk8r_UQNn95RLUhBXAJE_aAFnI3nfdL_FncWul_JqHXDsblQZOTnm2TRrSxAMzDbu7H6MJ2H2LbWOOHGAiSf8IZxMWOXJev33RRe2fGKyj8tNVgGjokwYdnNbT6MI2V11yklMqUPQMaJpAUkuUlj9w-omb3llL0plsBNUHsPPQ-63Zt-OT_i1i3K07RHBi_lzKk_23AJ6kZybO3bqKh57Fm3k8Td8bHpD8c9mnHthlGTgnG6vxayEH1gZ5kdouu443Y39M9v6jND0mqSiGCoBIK4feUVjEKjzG20cF7WhbGQBTd04SRaLcCaS9tXeIye5p0-6Kh9K4CD1XM0EnmE8JCR81UlaFr1b1Ou-q6m37E9CIUCVNSDT699Dvv5cj97qJotu9oA17CvVIaV0H9te3TnafTAMepPT03aBOFlaX6zKuV4TxFrpqSBYcPzkG2ek-XITDtAWE_0GFDTajPaTmD-2Lksb6wMmla_gZYl58oCT01Ze8nAsIXmsKPMywEeIHTGPVI6; 1P_JAR=2021-09-28-15; ANID=AHWqTUmTm5iBdRbl0pirNTP0WWU64d9o6iblGeKMLj23NMVIX8r3-g0lNVgQ6QdW; SID=CAioqz6Il9ir-u3aREgIG8TqxDGDan7-gEIRy-mFsEEKQk1SOHlZNLf2WOqWryrA8rr3dQ.; __Secure-3PSID=CAioqz6Il9ir-u3aREgIG8TqxDGDan7-gEIRy-mFsEEKQk1Sxy9xAv4Otr-xCj7LYA7G5g.; HSID=AFOk9UkjoxxDYneYl; SSID=APEOUwvBjrwiN3HSN; APISID=Krmc5kE3_0wdynWi/AwQAS_UiH7SLAB2d9; SAPISID=aylabutMIzwEqrYl/AlumFxn5cdRkPEO0H; __Secure-3PAPISID=aylabutMIzwEqrYl/AlumFxn5cdRkPEO0H; SIDCC=AJi4QfGRU7lOUTNOB1cIfBK06znXBvDjPlnmWWCykA9vPBj9moJHrKBVUsDjN2M9-7YImV9lHA_C; SEARCH_SAMESITE=CgQI7ZIB; __Secure-1PSID=CAioqz6Il9ir-u3aREgIG8TqxDGDan7-gEIRy-mFsEEKQk1S_gK14ez2VaqEuzPLExVwsg.; __Secure-1PAPISID=aylabutMIzwEqrYl/AlumFxn5cdRkPEO0H; __Secure-3PSIDCC=AJi4QfF930uxT-WMl_ggZNm6rdeykHz8SRyCdgFkTDY0gcP57Yglk_UpPVbzFyBRQCX8-bhyPGZX; OTZ=6155360_24_24__24_; OGPC=19025836-2:; GOOGLE_ABUSE_EXEMPTION=ID=31a92bd559cc6a1e:TM=1632842203:C=r:IP=124.106.130.232-:S=SL35BK3uR7kEtyzO3HkSPZY; DV=01_uKYrXMkweYPXf0FOdhZBXjU7Pw'
    #Run scraper
    scraper = GoogleScraper(keyword, pages, cookies)
    scraper.run()
