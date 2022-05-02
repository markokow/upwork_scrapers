import csv
import requests
import io
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
from random import randint
from time import sleep

class GardeningTips:
    def __init__(self, *,urls: List = [], max_divisions: int = 3) -> None:
        '''Initialize variables used for scraping.'''
        self.urls: List = urls
        self.url: str = ""
        self.max_divisions = max_divisions

        self.base_url: str = 'https://www.google.com/search'
        self.result: List = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }

        self.csv_headers = [None]

    def fetch(self):
        '''Fetch the url and returns bs4 object.'''
        response = requests.get(self.url, headers = self.headers)

        return response

    def parse(self, *, html) -> str:
        '''Parse the urls contained in the page and append to results.'''
        content = BeautifulSoup(html, 'lxml')

        features: dict = {}
        all_answers = content.find("div",{"id":"tdi_62"})
        all_answers = all_answers.find("div",{"class":"tdb-block-inner"})
        
        final_answer: str = ''
        to_remove: str = ''
    
        if all_answers:
            # final_answer = all_answers.text.strip()
            final_answer = str(all_answers)
            remove = content.find("div",{"class": "lwptoc_i"})

            image_urls = all_answers.find_all("img")
            video_urls = all_answers.find_all("video")
  
            if remove:
                # to_remove = remove.text.strip()
                to_remove = str(remove)
                final_answer = final_answer.replace(to_remove, " ")

            features['url'] = self.url
            features["title"] = content.title.text.strip()
            code_blocks = all_answers.find_all("div", {"class": "code-block"})

            for code in code_blocks:
                final_answer = final_answer.replace(str(code), "")
            features["content"] = final_answer

            if final_answer != "":
                self.result.append(features)
                for idx, img in enumerate(image_urls):
                    features[f"img_src_{idx+1}"] = img.get("src")

                for idx, vid in enumerate(video_urls):
                    features[f"vid_src_{idx+1}"] = vid.get("src")

                if len(features.keys()) > len(self.csv_headers):
                    self.csv_headers = features.keys()

                return True
            else:
                return False
        
        return False


    def write_csv(self, file_name: str = ''):
        '''Save results to csv.'''
        print('Saving to csv....')

        imgs = [_ for _ in self.csv_headers if "img_src" in _]
        vids = [_ for _ in self.csv_headers if "vid_src" in _]

        new_headers = list(self.csv_headers)[:3] + imgs + vids

        if self.result: 
            with open(f'{file_name}', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = new_headers)
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)

        print(f"Saved to {file_name}")

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
        '''Run all cases using the urls'''
        self.now = str(datetime.today()).replace(':','-')
        print("Scraping is running please don't exit...")
        counter = 0
        part = 0
        actual_counter = 0

        for url in self.urls:

            sleep(randint(1,2))
            
            self.url = url
            resp = self.fetch()
            print(self.url)
            _boolean = self.parse(html = resp.content)
            actual_counter += 1

            # self.write_csv(file_name = "test2.csv")
            if _boolean:   
                counter+=1
                if counter % self.max_divisions == 0:
                    part+=1 
                    self.write_csv(file_name = f"{self.now}_part{part}.csv")
                    self.csv_headers = [None]
                    self.result = []
                    continue
                else:
                    if (len(self.urls) - counter) > self.max_divisions:
                        continue
                    else:
                        if actual_counter == len(self.urls):
                            part += 1 
                            self.write_csv(file_name = f"{self.now}_part{part}.csv")
                            break
                        else:
                            continue

            if actual_counter == len(self.urls):
                part += 1
                self.write_csv(file_name = f"{self.now}_part{part}.csv")


if __name__ == '__main__':
    '''Run main file.'''
    file =  open('garden_urls.txt', 'r', encoding='utf-8')
    urls: List = [acc.strip() for acc in file.readlines()]
    max_divisions: int = 3
    
    #Run scraper
    scraper = GardeningTips(urls= urls, max_divisions = max_divisions)
    scraper.run()
