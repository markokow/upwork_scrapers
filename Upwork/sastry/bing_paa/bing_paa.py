from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import csv
import requests
import io
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime

class Bing_PAA:
    def __init__(self, *,keywords: List = [], max_questions: int = 5) -> None:
        '''Initialize variables used for scraping.'''
        self.keywords: List = keywords
        self.keyword: str = ""
        self.query: str = ""
        self.max_questions: int = max_questions

        self.base_url: str = 'https://www.google.com/search'
        self.result: List = []

        self.snippets_total: List = [self.keyword]
        self.parsed_snippet: List = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }

    def get_useragent(self):
        '''Gets the user agent using the os.'''
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=1000)
        return user_agent_rotator.get_random_user_agent()

    def fetch(self):
        '''Fetch the url and returns bs4 object.'''
        self.headers['User-Agent'] = self.get_useragent()
        response = requests.get(f"https://www.bing.com/search?q='+{self.keyword}", headers = self.headers)

        return response

    def parse(self, *, html) -> str:
        '''Parse the urls contained in the page and append to results.'''
        content = BeautifulSoup(html, 'lxml')

        paa_block = content.find("div", {"id": "relatedQnAListDisplay"})
        paa_questions = paa_block.find_all("div", {"class": "df_topAlAs df_sideColor df_alsoAsk df_close"})

        for paa_question in paa_questions:

            question = paa_question.find("div", {"class": "b_expansion_text b_1linetrunc"})
            question = question.text.strip() if question else ""

            if question.endswith('?'):
                self.snippets_total.append(question)

        answer = content.find("div", {"class":"rwrl rwrl_pri rwrl_padref"})

        image_tt = content.find("div", {"id":"qna_imgtt_tt"})
        image = content.find("div", {"id":"qna_imgtt_img"})

        image_tt = image_tt.text.strip() if image_tt else " "
        image = image.text.strip() if image else " "

        _answer = answer.text.strip()

        if len(image) not in [1,0]:
            _answer = _answer.replace(image, "")
        if len(image_tt) not in [1,0]:
            _answer = _answer.replace(image_tt, "")

        return _answer

    def write_csv(self):
        '''Save results to csv.'''
        print('Saving to csv....')

        now = str(datetime.today()).replace(':','-')

        if self.result: 
            with open(f'{now}.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)

        print(f"Saved to {now}.csv")
    
    def open_csv(self):
        '''Opens a csv.'''
        print("opening csv")
        with open('results.csv', 'r', newline = '', encoding= 'utf-8') as csv_file:
            _dict_reader = csv.DictReader(csv_file)
            self._taken = list(_dict_reader)
        

        self._done = [_val['valid_urls'] for _val in self._taken]

        self.result = self._taken

        print(self.result)


    def store_response(self, *,response, page):
        '''Saved response as html.'''
        if response.status_code == 200:
            print('Saving response as html')
            filename = 'res' + str(page) + '.html'
            with io.open(filename, 'w', encoding = 'utf-8') as html_file:
                html_file.write(response.text)
            print('Done')
        else:
            print('Bad response!')
  
    def load_response(self):   
        '''Load an html file.'''
        html = ''
        with open('res.html', 'r') as html_file:
            for line in html_file.read():
                html += line
        return html

    def run(self):
        '''Run all cases using the keyword'''   

        try:
            for keyword in self.keywords:

                current_total: int  = 0

                self.query = keyword
                self.keyword = keyword
                self.snippets_total = [keyword]
                self.parsed_snippet = []

                output_dict: dict = {}
                output_dict['keyword'] = self.query

                while True:

                    for snip in self.snippets_total:
                        if snip not in self.parsed_snippet:
                            self.keyword = snip
                            self.parsed_snippet.append(snip)
                            break
                        else:
                            continue
                            
                    resp = self.fetch()

                    try:
                        ans = self.parse(html  = resp.content)
                    except AttributeError:
                        continue
                    self.parsed_snippet.append(self.keyword)

                    if len(ans) < 50:
                        continue

                    if self.keyword == self.query:
                        # self.store_response(response=resp, page = 0)
                        continue
                    else:
                        current_total += 1
                        output_dict['question_' + str(current_total)] = self.keyword
                        output_dict['answer_' + str(current_total)] = ans

                    if current_total == self.max_questions:
                        break

                    print(self.keyword)

                self.result.append(output_dict)
        
        except KeyboardInterrupt:
            pass

        finally:
            self.write_csv()

if __name__ == '__main__':  
    file =  open('keywords.txt', 'r', encoding='utf-8')
    keywords: List = [acc.strip() for acc in file.readlines()]
    max_questions: int = 5

    #Run scraper
    scraper = Bing_PAA(keywords= keywords, max_questions = max_questions)
    scraper.run()