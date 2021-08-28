import csv
import requests
from bs4 import BeautifulSoup
import io
from datetime import datetime
from urllib.request import urlopen, Request
import re

class ScrapeWebsite:

    result = []

    def setup(self, url):

        try:
        #     page = urlopen(url) 
        #     self.start_scrape(page, url)
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(url, headers=hdr)
            page = urlopen(req)
            return self.start_scrape(page, url)
        except:
            print('Request denied for url:', url)


    def start_scrape(self, page, url):
        
        print("Searching:",url)
        scrape = BeautifulSoup(page, 'html.parser')
        scrape = scrape.get_text() 

        phone_numbers = set(re.findall(r"((?:\d{3}|\(\d{3}\))?(?:\s|-|\.)?\d{3}(?:\s|-|\.)\d{4})", scrape)) #"set" removes duplicates
        emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}", scrape)) 

        nodupnumber = len(list(phone_numbers))
        nodupemail = len(list(emails))

        dupnumber = len(list(re.findall(r"((?:\d{3}|\(\d{3}\))?(?:\s|-|\.)?\d{3}(?:\s|-|\.)\d{4})", scrape))) 
        dupemail = len(list(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}", scrape)))

        number_of_dup_number = int(dupnumber) - int(nodupnumber) 
        number_of_dup_email = int(dupemail) - int(nodupemail)

        email_list = list(emails)
        phone_numbers_list = list(phone_numbers)

        if len(phone_numbers) == 0:
            print("No phone number(s) found in:", url)
        else:
            count = 1
            for item in phone_numbers:
                self.result.append(
                    {'number': item}
                )
                # print("Phone number #" + str(count) + ': ' + item)
                count += 1

            print("\tTotal phone numbers: ", nodupnumber)


        # print("-----------------------------\n")

        # if len(emails) == 0:
        #     print("No email address(es) found in:", url)
        #     # print("-----------------------------\n")
        # else:
        #     count = 1
        #     for item in emails:
        #         self.result.append(
        #             {'email': item}
        #         )
        #         # print('Email address #' + str(count) + ': ' + item)
        #         count += 1
        #     print("\tTotal emails found: ", nodupemail)


        # if save_excel:
        #     for email,phone in zip(email_list,phone_numbers_list):
        #         sheet.append({'emails:':email, 'phone':phone})
        #     excel_file = (name_the_file + ".xlsx")
        #     book.save(excel_file) 
        
        # print("\n\tDuplicates have been removed from list.")
        # print("\tTotal email addresses: ", nodupemail)
        # print("\tThere were " + str(number_of_dup_number) + " duplicate phone numbers.")
        # print("\tThere were " + str(number_of_dup_email) + " duplicate email addresses.")
        return self.result

        # if save_excel:
        #     print("\n\nData has been stored inside of an Excel spreadsheet named: "
        #         + excel_file + " in this directory: " + os.getcwd())
        #     mod_time = os.stat(excel_file).st_mtime
        #     print("\nCompleted at: " + str(datetime.fromtimestamp(mod_time)))
        #     print("\nSize of file: " + str(os.stat(excel_file).st_size) + " KB")


class GoogleScraper:

    base_url = 'https://www.google.com/search'
    keyword = 'query'
    keyword_list = []

    pagination_params = {
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

    headers = {
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

    result = []

    def fetch(self, page):
        self.pagination_params['start'] = str(10*page)
        self.pagination_params['q'] = self.keyword
        self.pagination_params['oq'] = self.keyword
        response = requests.get(self.base_url, params = self.pagination_params, headers = self.headers)
        return response

    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        # print('Crawling the net with keyword', self.keyword)
        for val in content.find_all('a'):
            link = val.get('href')
            title = val.text
            if link not in [None,'#', ''] and link.startswith('http') and title not in [None, '']:
                check = bool([ele for ele in self.keyword_list if(ele in link)]) and bool([ele for ele in self.keyword_list if(ele in title)])
                if check:
                    web_scraper = ScrapeWebsite()
                    res = web_scraper.setup(link.replace(' ',''))
                    if res is not None:
                        self.result.extend(res)
                    else:
                        continue
                    # self.result.append({
                    #     'title': val.text,
                    #     'links': link.replace(' ',''),
                    #     'timestamp': datetime.now()
                    # })
                else:
                    continue

    def write_csv(self,):
        # for item in self.result:
        #     print(item['number'])

        print('Saving to csv....')
        if self.result: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)
        print("Saved to results.xlsx")
        

    def store_response(self, response, page):
        if response.status_code == 200:
            print('Saving response as html')
            filename = 'res' + str(page) + '.html'
            with io.open(filename, 'w', encoding = 'utf-8') as html_file:
                html_file.write(response.text)
            print('Done')
        else:
            print('Bad response!')
  
    def load_response(self,):
        html = ''
        with open('res.html', 'r') as html_file:
            for line in html_file.read():
                html += line
        return html
        

    def run(self,):
        self.keyword = input('Enter your keyword: ')
        self.keyword_list = [x.lower() for x in self.keyword.split()]
        pages = input('Number of pages: ')
        for page in range(1,int(pages)+1):
            resp = self.fetch(page-1)
            # self.store_response(resp,page)
            self.parse(resp.content)
        self.write_csv()

if __name__ == '__main__':
    scraper = GoogleScraper()
    scraper.run()
