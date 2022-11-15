import re
import io
import os
import requests
from typing import List
from datetime import datetime
from requests_html import HTMLSession
from bs4 import BeautifulSoup, NavigableString, Tag
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from boilerpy3 import extractors
from urllib.error import HTTPError

disable_warnings(InsecureRequestWarning)

class SERP:

    def __init__(self, *,KEYWORD_LIST: List = [],FOLDER_NAME: str = '') -> None:
        '''Initialize variables used for scraping.'''
        self.KEYWORD_LIST: List = KEYWORD_LIST
        self.FOLDER_NAME: str = FOLDER_NAME
        self.base_url: str = 'https://www.google.com/search'
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }
        self.keyword: str = ''
        self.VERIFY = True


    def get_source(self, url):
        """Return the source code for the provided URL. 
        Args: 
            url (string): URL of the page to scrape.
        Returns:
            response (object): HTTP response object from requests_html. 
        """
        try:
            session = HTMLSession()
            response = session.get(url, verify=self.VERIFY)
            return response

        except requests.exceptions.RequestException as e:
            print(e)


    def store_response(self, *,response, filename: str = ''):
        '''Saved response as html.'''
        if response.status_code == 200:
            print('Saving response as html')
            with io.open(f"{filename}.html", 'w', encoding = 'utf-8') as html_file:
                html_file.write(response.text)
            print('Done')
        else:
            print('Bad response!')

    def find_between(self, s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return f"<b>{first}</b>" + s[start:end]
        except ValueError:
            return ""


    def get_text(self, tag) -> str:
        _inline_elements = {"a","span","em","strong","u","i","font","mark","label","s","sub","sup","tt","bdo","button","cite","del","b","a","font"}
        def _get_text(tag):
        
            for child in tag.children:
                if type(child) is Tag:
                    # if the tag is a block type tag then yield new lines before after
                    is_block_element = child.name not in _inline_elements
                    if is_block_element: yield ""
                    yield from ["\n"] if child.name=="br" else  _get_text(child)
                    if is_block_element: yield "\n"
                elif type(child) is NavigableString:
                    yield child.string
        return "".join(_get_text(tag))


    def text_with_newlines(self, elem):
        text = ''
        for e in elem.descendants:
            if isinstance(e, str):
                text += e.strip()
            elif e.name == 'br' or e.name == 'p':
                text += '\n'
        return text


    def walk_main_url(self, *, url):
        '''Checks the main url pull from serp.'''
        sub_reps = self.get_source(url = url)
        if sub_reps == None:
            return None

        extractor = extractors.CanolaExtractor()
        try:
            doc = extractor.get_doc_from_url(url)
        except TypeError:
            return None

        txt_lst = []
        content = BeautifulSoup(sub_reps.content, 'lxml')

        header_list = content.find_all(["h2", "h3", "h1"])
        header_list = [_.text.strip() for _ in header_list]
        header_list = [_ for _ in header_list if ((len(_) > 12) and (len(_) < 50))]
        content_txt = doc.content
        content_txt = re.sub(r"\n+", "\n\n", content_txt)
        if header_list:
            first_title = header_list[0]
            header_list = [_ for _ in header_list if _ in content_txt]
            header_list = [[header_list[i], header_list[i+1]] for i in range(len(header_list)-1)]
            # header_list = header_list[:4] if len(header_list) > 3 else header_list
            if len(header_list) > 1:
                counter = 0
                for header in header_list:
                    if counter >= 3:
                        break
                    text = self.find_between(content_txt, header[0], header[-1])
                    if text.strip() == "":
                        continue
                    else:
                        txt_lst.append(text)
                        counter += 1
            else:
                txt_lst = [f"<b>{first_title}</b>" + content_txt]
        else:
            txt_lst = [content_txt]

        return txt_lst


    def parse(self, *, html) -> str:
        '''Parse the urls contained in the page and append to results.'''
        content = BeautifulSoup(html, 'lxml')
        total_counter: int = 0

        answer = content.find_all("div", {"class": "yuRUbf"})
        # answer = answer[:3] if len(answer) > 3 else answer
        vids = content.find_all("a", {"class": "X5OiLe"})
        vids = [_.get('href') for _ in vids][::-1]

        article_txt: str = ''
        for ans in answer:
            url = ans.find('a')['href']
            print(f"Pulling data from: {url}")
            try:
                txt_lst = self.walk_main_url(url = url)
            except HTTPError:
                print("Error! Url not available.")
                continue
            if total_counter >= 3:
                break

            if txt_lst:
                total_counter += 1
                for txt in txt_lst:
                    vid_link: str = ''
                    try:
                        vid_link = vids.pop()
                    except:
                        pass
                    article_txt += txt.strip() + '\n' +  vid_link + '\n'
                article_txt += '\n' + url + '\n'

        with open(f"{self.FOLDER_NAME}/{self.keyword}.txt", "w") as text_file:
            text_file.write(article_txt)


    def run(self):
        '''Run all cases using the keyword'''  
        output_folder_path = os.path.join(os.getcwd(), self.FOLDER_NAME)
        if not(os.path.exists(output_folder_path)):
            os.makedirs(output_folder_path)

        for keyword in self.KEYWORD_LIST:
            self.keyword = keyword
            url = f"https://www.google.com/search?q=+'{keyword}"
            resp = self.get_source(url = url)
            self.parse(html = resp.content)


if __name__ == '__main__':
    file =  open('keywords.txt', 'r', encoding='utf-8')
    KEYWORD_LIST: List = [acc.strip() for acc in file.readlines()]
    FOLDER_NAME = str(datetime.today()).replace(':','-')
    #Run scraper
    scraper = SERP(KEYWORD_LIST= KEYWORD_LIST, FOLDER_NAME=FOLDER_NAME)
    scraper.run()