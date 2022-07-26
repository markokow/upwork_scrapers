from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import csv
import requests
import io
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
from requests_html import HTMLSession
import urllib
import requests_html
import re
from dateutil.parser import parse
import pandas as pd
from tomlkit import key
import time

class Bing_Google_PAA_Merge:
    def __init__(self, *,keywords: List = [], max_divisions: int = 5, max_bing: int = 4, max_paa: int = 10) -> None:
        '''Initialize variables used for scraping.'''
        self.keywords: List = keywords
        self.main_keyword: str = ""
        self.keyword: str = ""
        self.query: str = ""
        self.max_divisions: int = max_divisions
        self.max_bing:int = max_bing
        self.max_paa:int = max_paa

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

    def google_fetch_query(self, query):

        query = urllib.parse.quote_plus(query)
        response = self.get_source(f"https://www.google.com/search?q={query}?")

        if response.status_code != 200:
            print(f"Error! with status code: {response.status_code}")

        return response

    def google_parse_response(self, response: requests_html.HTMLResponse = None):

        content = BeautifulSoup(response.content, 'lxml', from_encoding="utf-8")

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

    def bing_fetch(self):
        '''Fetch the url and returns bs4 object.'''
        self.headers['User-Agent'] = self.get_useragent()
        response = requests.get(f"https://www.bing.com/search?q='+{self.keyword}", headers = self.headers)

        return response

    def bing_parse(self, *, html) -> str:
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

    def bing_run(self,):

        current_total: int  = 0

        self.query = self.main_keyword
        self.keyword = self.main_keyword
        self.snippets_total = [self.main_keyword]
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
                    
            resp = self.bing_fetch()

            try:
                ans = self.bing_parse(html  = resp.content)
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
                output_dict['bing_question_' + str(current_total)] = self.keyword
                output_dict['bing_answer_' + str(current_total)] = ans

            if current_total == self.max_bing:
                break

        return output_dict

        # self.result.append(output_dict)

    def google_run(self,):

        self.query = self.main_keyword
        self.keyword = self.main_keyword
        self.snippets_total = [self.main_keyword]
        self.parsed_snippet = []

        question_counter: int = 0

        output_dict: dict = {'keyword': self.query}

        while self.snippets_total:

            if question_counter == self.max_paa:
                return output_dict
                # self.result.append(output_dict)
                # break

            for snip in self.snippets_total:
                if snip in self.parsed_snippet:
                    continue

                self.keyword = snip
                break
            time.sleep(3)
            response = self.google_fetch_query(query = self.keyword)
            result = self.google_parse_response(response = response) 

            if result is None:
                if (self.keyword == self.main_keyword) &  (len(self.snippets_total) == 1):
                    break
                self.parsed_snippet.append(self.keyword)
                continue
            else:
                self.parsed_snippet.append(self.keyword)
                question_counter+=1
                output_dict[f'google_question_{question_counter}'] = self.keyword
                output_dict[f'google_answer_{question_counter}'] = result


                if (self.keyword == self.main_keyword) &  (len(self.snippets_total) == 1):
                    return output_dict

        return output_dict
                    

    def store_response(self, response, query_name):
        '''Saved response as html.'''
        # if response.status_code == 200:
        print('Saving response as html')
        filename = query_name + ".html"
        with io.open(filename, 'w', encoding = 'utf-8') as html_file:
            html_file.write(response.text)
            print('Done')

    def parse_vids(self, query):

        resp = self.google_fetch_query(query=self.main_keyword)
        content = BeautifulSoup(resp.content, 'lxml', from_encoding="utf-8")

        all_vids = content.find("div", {"class": "o0igqc"})
        output_dict: dict = {}

        if all_vids:
            vids = all_vids.find_all("div", {"class": "RzdJxc"})
            if vids:
                for idx, vid in enumerate(vids):
                    link = vid.find("a", {"class": "X5OiLe"})
                    if link:
                        link = link['href']
                        output_dict[f"video_{idx+1}"] = link

                    if idx == 2:
                        break
        
        return output_dict

    def run(self):
        '''Run all cases using the keyword'''  

        counter: int = 0
        part: int = 0

        self.now = str(datetime.today()).replace(':','-')

        for count, keyword in enumerate(self.keywords):
            print(keyword)
            self.main_keyword = keyword
            bing_res = self.bing_run()
            google_res = self.google_run()
            try:
                output = {**bing_res, **google_res}
            except:
                output = {'keyword':self.main_keyword}
            vid_res = self.parse_vids(query=self.main_keyword)

            try:
                output = {**output, **vid_res}
            except:
                continue
            
            if (len(output.keys())) > 1:
                counter += 1
                self.result.append(output)
            else:
                continue

            if count == len(self.keywords) - 1:
                part += 1
                df_out = pd.DataFrame(self.result)
                df_out.to_csv(f"{self.now}_part{part}.csv", index = False)
                print(f"Saving {self.now}_part{part}.csv")
                break
            
            if (counter % self.max_divisions) == 0:
                part += 1
                df_out = pd.DataFrame(self.result)
                df_out.to_csv(f"{self.now}_part{part}.csv", index = False)
                print(f"Saving {self.now}_part{part}.csv")
                self.result = []
            else:
                continue


if __name__ == '__main__':  
    file =  open('keywords.txt', 'r', encoding='utf-8')
    keywords: List = [acc.strip() for acc in file.readlines()]
    max_divisions: int = 20
    max_bing: int = 4
    max_paa: int = 10

    #Run scraper
    scraper = Bing_Google_PAA_Merge(keywords= keywords, max_divisions = max_divisions, max_bing=max_bing, max_paa=max_paa)
    scraper.run()