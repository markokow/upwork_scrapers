import pandas as pd
import requests
import io
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List

class ByJus_Scraper:

    def __init__(self, *,urls: List = []) -> None:
        '''Initialize variables used for scraping.'''
        self.urls: List = urls
        self.url: str = ''

        self.result: List = []

        self.parsed_urls: List = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }

    def fetch(self):
        '''Fetch the url and returns bs4 object.'''
        print(self.url)
        response = requests.get(self.url, headers = self.headers)

        return response

    def parse(self, *, html) -> str:
        '''Parse the urls contained in the page and append to results.'''
        feature: dict = {}
        content = BeautifulSoup(html, 'html5lib')

        _final_question: str = ''
        _final_answer: str = ''

        question_list: List = []

        question_block = content.find("h1", {"class": "text_contentH1__2_8-o"})
        questions_bullets = question_block.find_all("li")
        question_list = [dat.text for dat in questions_bullets]

        _final_question = content.title.text + '\n' + "\n".join(question_list) if question_list else question_block.text
        
        answer_block = content.find("h2", {"class": "text_contentH1__2_8-o"})
        _divs = answer_block.find_all("div")

        if _divs:
            for _div in _divs:   

                _div_data: str = _div.text if _div.text != None else ''

                try:
                    _first_br_element = _div.next_element.strip()
                except:
                    _first_br_element = None

                _brs = _div.find_all('br')
                _br_data: str = ''
                
                if _brs:
                    for _br in _brs:

                        try:
                            _br_strip = _br.next_element.strip()
                        except:
                            _br_strip = ''
                        
                        _br_data += _br_strip

                        if _br_strip in _div_data:
                            _div_data = _div_data.replace(_br_strip, '')

                    _final_answer += _div_data + ('\n' if _first_br_element else '') +  _br_data

                else:
                    _lists = _div.find_all("li")
                    if _lists:
                        _li_string = '\n'.join(dat.text for dat in _lists)
                        _final_answer += ('\n' if _final_answer != '' else '') + _li_string
                    else:
                        _final_answer += ('\n' if _final_answer != '' else '')  + _div.text

        else:
            _final_answer = answer_block.text

        _split = _final_answer.split('\n')

        _final_answer_2: str = ''
        
        try:
            if _split[1] in _split[0]:
                _final_answer_2 = '\n'.join(_final_answer.split('\n')[1:])
            else:
                _final_answer_2 = _final_answer
        except IndexError:
            _final_answer = _final_answer


        if _final_answer_2 == '':
            _final_answer_2 = _final_answer

        feature = {
            'url': self.url,
            'question':_final_question.strip(),
            'answer': _final_answer_2.strip()
        }

        self.result.append(feature)

    def write_excel(self):
        '''Save results to excel.'''
        print('Saving to excel....')
        now = str(datetime.today()).replace(':','-')
        df = pd.DataFrame(self.result)
        df.to_excel(f'{now}.xlsx', encoding='utf-32', index = False)

        print(f"Saved to {now}.xlsx")
    
    def store_response(self, *, response, page):
        '''Saved response as html.'''
        if response.status_code == 200:
            print('Saving response as html')
            filename = 'res' + str(page) + '.html'
            with io.open(filename, 'w', encoding = 'utf-8') as html_file:
                html_file.write(response.text)
            print('Done')
        else:
            print('Bad response!')

    def run(self):
        '''Run all cases using the keyword'''
        counter = 0
        for url in self.urls:
            self.url = url
            resp = self.fetch()
            # self.store_response(response=resp, page = counter)
            self.parse(html = resp.content)
            counter += 1

        self.write_excel()

if __name__ == '__main__':

    file =  open('inputs.txt', 'r', encoding='utf-8')
    urls: List = [acc.strip() for acc in file.readlines()]

    #Run scraper
    scraper = ByJus_Scraper(urls= urls)
    scraper.run()
