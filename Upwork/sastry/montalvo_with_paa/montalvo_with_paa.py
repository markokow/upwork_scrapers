import io
import re
import csv
import requests
import urllib
import pandas as pd
import requests_html
from typing import List
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
from requests_html import HTMLSession
from os import path
import glob
import os


class CombinedPaa_Montalvo:

    def __init__(self, *, max_paa: int = 4, max_divisions: int = 3) -> None:
        '''Initialize variables used for scraping.'''
        self.paa_keyword: str = ""
        self.stack_url: str = ""
        self.max_paa: int = max_paa
        self.max_divisions: int = max_divisions
        self.result: List = []
        self.snippets_total: List = []
        self.parsed_snippet: List = []
        self.csv_headers = [None]

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }


    def cleanup(self, string):

        patterns = [
            # r"{2}-{1:0>2}-{0:0>2}",   
            # r"{0}-{1:0>2}-{2:0>2}",
            # r"{0}-{1:0>2}",
            r"\d{2}-(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{4}",
            r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d, \d{4}",
            r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2}, \d{4}",
        ]

        for pattern in patterns:
            string = re.sub(pattern, '', string)

        return string

    def get_source(self, url):
        """Return the source code for the provided URL. 

        Args: 
            url (string): URL of the page to scrape.

        Returns:
            response (object): HTTP response object from requests_html. 
        """
        try:
            session = HTMLSession()
            response = session.get(url)
            return response

        except requests.exceptions.RequestException as e:
            print(e)

    def store_response(self, response, query_name):
        '''Saved response as html.'''
        # if response.status_code == 200:
        print('Saving response as html')
        filename = query_name + ".html"
        with io.open(filename, 'w', encoding = 'utf-8') as html_file:
            html_file.write(response.text)
            print('Done')

    def fetch(self, url):
        '''Fetch the url and returns bs4 object.'''
        response = requests.get(url, headers = self.headers)

        if response.status_code != 200:
            print(f"Status code: {response.status_code}")
            print("Error! Please exit scraper and wait a few hours.")

        return response

    def parse(self, *, html) -> str:
        '''Parse the urls contained in the page and append to results.'''
        content = BeautifulSoup(html, 'lxml')

        features: dict = {}
        
        # _data = content.find("div", {"id":"primary"})
        _data = content.find("div", {"class":"entry-content"})
        title = content.title.text.strip()
        # title = title.replace("\"", "")
        # title = title.replace("'", "")

        # print(_data)

        # print(title )

        if _data:

            _eztoc = _data.find("div", {"id":"ez-toc-container"})
            _code_blocks = _data.find_all("div", {"class":"code-block"})
            _youtube_ads = _data.find_all("div", {"class":"rll-youtube-player"})

            if _eztoc:
                _content = str(_data).replace(str(_eztoc), "")
            else:
                _content = str(_data)

            if _code_blocks:
                for  _code in _code_blocks:
                    _content = str(_content).replace(str(_code), "")
                # idx = self.find_str(s = _content, char = '<div class="code-block code-block-9">')

                # if idx != -1:
                #     _content = _content[:idx]
            if _youtube_ads:
                for  _ad in _youtube_ads:
                    _content = str(_content).replace(str(_ad), "")

            # _content = _content.replace("<div class=\"entry-content\">\n", "<div class=\"entry-content\">")
            _content = _content.replace("<div class=\"entry-content\">\n", "")

            idx = self.find_str(s = _content, char = '<!-- AI CONTENT END 2 -->')
            _content = _content[:idx]
            _content = _content.strip()
            
            # print(_content.strip())

        #     _content = str(_data)
        #     idx = self.find_str(s = _content, char = '<p><span data-sheets-userformat=')
        #     if idx != -1:
        #         _content = _content[:idx]
        #     else:
        #         idx = self.find_str(s = _content, char = '<div class="addtoany_share_save')

        #         if idx != -1:
        #             _content = _content[:idx]


            features['url'] = self.url
            features['title'] = title
            features["content"] = _content.strip()


        return (features if _data else None)

    def find_str(self, *, s, char):
        index = 0

        if char in s:
            c = char[0]
            for ch in s:
                if ch == c:
                    if s[index:index+len(char)] == char:
                        return index

                index += 1

        return -1


    def fetch_query(self, query):

        query = urllib.parse.quote_plus(query)
        response = self.get_source("https://www.google.com/search?q='"+query+"?")

        if response.status_code != 200:
            print(f"Status code: {response.status_code}")
            print("Error! Please exit scraper and wait a few hours.")

        return response


    def parse_response(self, response: requests_html.HTMLResponse = None):

        # content = BeautifulSoup(response.content, 'lxml', from_encoding="utf-8")
        content = BeautifulSoup(response.content, 'lxml')


        answer = content.find("div", {"class": "V3FYCf"})
        lists: str = ''

        ppl_also_ask = content.find("div", {"jsname": "N760b"})

        if ppl_also_ask:
            all_paas = ppl_also_ask.find_all("div", {"jsname": "Cpkphb"})

            for paa in all_paas:

                data = paa.find("div", {"jsname": "F79BRe"})
                self.snippets_total.append(data["data-q"])

        if answer:
            heading = answer.find("div", {"role":"heading"})
            try:
                lists = "\n".join([val.text.replace("...", "").strip() for val in  answer.find_all("li") if val])
                if lists == None:
                    lists = ""
            except AttributeError:
                lists = ""

            if heading:
                try:
                    texts: List = []

                    for val in heading.find_all("span"):
                        text = val.text.strip()
                        texts.append(text)

                    texts = list(set(texts))
                    texts = "\n".join(texts)

                    answer = texts + lists
                    try:
                        answer = parse(answer, fuzzy_with_tokens=True)[1]
                        answer = ''.join([x for x in answer if x != ' '])
                    except:
                        answer = answer
                    return self.cleanup(answer).strip()
                except AttributeError:
                    try:
                        lists = parse(lists, fuzzy_with_tokens=True)[1]
                        lists = ''.join([x for x in lists if x != ' '])
                    except:
                        lists = lists
                    return self.cleanup(lists).strip()
            else:
                return None
        else:
            return None


    def write_csv(self, file_name: str = ''):
        '''Save results to csv.'''
        print('Saving to csv....')

        if self.result: 
            with open(f'{file_name}.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.csv_headers)
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)

        print(f"Saved to {file_name}.csv")

    def sub_paa(self, keyword: str = ""):
    
            # sleep(randint(2,3))
        self.paa_keyword = keyword
        self.snippets_total = [keyword]
        self.parsed_snippet = []

        question_counter: int = 0

        output_dict: dict = {}
        output_dict['keyword'] = keyword

        while self.snippets_total:

            if question_counter == self.max_paa:
                return output_dict
                # self.result.append(output_dict)
                # break

            for snip in self.snippets_total:
                if snip not in self.parsed_snippet:
                    self.paa_keyword = snip
                    break
                else:
                    continue

            response = self.fetch_query(query = self.paa_keyword)
          #  self.store_response(response=response, query_name=keyword)
            result = self.parse_response(response = response) 


            if result == None:
                if (self.paa_keyword == keyword) &  (len(self.snippets_total) == 1):
                    break
                else:
                    self.parsed_snippet.append(self.paa_keyword)
                    continue
            else:
                self.parsed_snippet.append(self.paa_keyword)
                question_counter+=1
                output_dict['question_' + str(question_counter)] = self.paa_keyword
                output_dict['answer_' + str(question_counter)] = result

                if (self.paa_keyword == keyword) &  (len(self.snippets_total) == 1):
                    return output_dict


    def sub_motalvo(self, url):
        self.url = url
        resp = self.fetch(url = url)
        result = self.parse(html = resp.content)
        
        return (result if result else None)

    def run(self):

        print("Scraper is running...")

        _path = "outputs"

        isExist = os.path.exists(_path)

        if not isExist:
        
        # Create a new directory because it does not exist 
            os.makedirs(_path)
            print("outputs folder is created!")
            
        if (path.isdir("inputs")):

            self.now = str(datetime.today()).replace(':','-')

            extension = 'txt'

            # lstJson = [f for f in os.listdir(str(self.pathJson)) if f.endswith('.txt')]
            # print
            data = glob.glob('inputs/*.{}'.format(extension))

            _final_urls: List = []
            for dat in data:
            # df = pd.read_csv("montalvo.csv", engine='python')
                print(dat)
                filename = dat
                _urls: List = []
                with open(dat) as f:
                    # _size = len(f.readlines())
                    lines = f.readlines()
                    _size = len(lines)

                    for line in lines:
                        _to_add = [line.strip(),filename, _size]
                        _urls.append(_to_add)
                    # _urls = [_.strip() for _ in f.readlines()]
                _final_urls.extend(_urls)

            final_res: List = []
            counter = 0
            part = 0
            current_loc: str = ''
            file_counter = 0
            _filename: str = ''

            # # for count, dat in enumerate(df.index):
            for count, dat in enumerate(_final_urls):
                file_counter += 1
                
                # sleep(randint(2,3))
                # url = df.iloc[dat,0]
                url = dat[0]
                loc = dat[1]
                _size = dat[2]

                # keyword = df.iloc[dat,1]
                # print(url, " ", keyword)
                # file_counter


                print(f"scraping: {url} located at: {loc} total urls scraped: {count+1}")
                montalvo_res = self.sub_motalvo(url = url)


                if loc != current_loc:
                    current_loc = loc
                    counter = 0
                    file_counter = 0
                    part = 0

                output = montalvo_res

                if output:
                    final_res.append(output)
                    counter += 1
                else:
                    continue

                if (count == (len(_final_urls) - 1)) | (file_counter == _size):
                    part += 1
                    df_out = pd.DataFrame(final_res)
                    _filename = f"{loc.strip('.txt').replace('inputs', 'outputs')}_part_{part}.csv"
                    df_out.to_csv(_filename, index = False)
                    print(f"Saving {_filename}")
                    if count == (len(_final_urls) - 1):
                        print("WHAT")
                        break
                
                if (counter % self.max_divisions) == 0:
                    part += 1
                    df_out = pd.DataFrame(final_res)
                    _filename = f"{loc.strip('.txt').replace('inputs', 'outputs')}_part_{part}.csv"
                    df_out.to_csv(_filename, index = False)
                    print(f"Saving {_filename}")
                    final_res = []
                else:
                    continue
        else:
            
            print("Inputs directory does not exist. Scraper will exit")

if __name__ == '__main__':

    max_paa: int = 3
    max_divisions: int = 5

    #Run scraper
    scraper = CombinedPaa_Montalvo(max_paa = max_paa, max_divisions = max_divisions)
    scraper.run()