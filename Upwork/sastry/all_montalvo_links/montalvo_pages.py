from unittest import result
import requests
from bs4 import BeautifulSoup
import glob
import csv
from datetime import datetime
from typing import List

results = []
saved_links = []
lines: List = []
lines_to_add: List = []

main_page = "www.montalvospirits.com"
file_name = str(datetime.today()).replace(':','-')
save_counter: int = 0
max_save: int = 50

def get_links(page_num):
    global pages
    global max_save
    global save_counter
    global results
    global lines
    global lines_to_add
    #   pattern = re.compile("^(/)")
    _headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    }

    proxy = {
        # 'https': 'https://41.217.219.53:31398'
    }
    page_url = f"https://www.montalvospirits.com/page/{page_num}/"
    html = requests.get(page_url, headers=_headers, proxies=proxy) # fstrings require Python 3.6+

    if html.status_code == 200:

        soup = BeautifulSoup(html.content, "html.parser")
        links = list(set([_["href"] for _ in soup.find_all("a", {"rel": "bookmark"}, href = True)]))

        for link in links:
            results.append(link)

        if len(results) > max_save:
            save_counter += 1
            with open(f'montalvo_result_{save_counter}.txt', 'w',  encoding='utf-8') as f:
                for item in results[:max_save]:
                    f.write("%s\n" % item)

            for line in lines_to_add:
                lines.append(line)

            lines_to_add = []
            results = results[max_save:]

            with open("parsed_pages.txt", 'w') as f:
                for item in lines:
                    f.write("%s\n" % item)
    else:
        print(html.status_code)

        # results = list(set(results))

        # to_save = []
        # if (len(results) - len(saved_links)) > max_save:
        #     for dat in links:
        #         if dat not in saved_links:
        #             saved_links.append(dat)
        #             to_save.append(dat)
        #             if len(to_save) == max_save:
        #                 break
        #     save_counter += 1
        #     with open(f'{file_name}_{save_counter}.txt', 'w') as f:
        #         for item in to_save:
        #             f.write("%s\n" % item)

    print(f"done: {page_url}")

def write_csv():
        print('Saving to csv....')

        if results: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = results[0].keys())
                writer_object.writeheader()

                for row in results:
                    writer_object.writerow(row)
        print("Saved to test.xlsx")


extension = 'txt'

data = glob.glob('*.{}'.format(extension))
try:
    last = [int(_.replace('.txt', '').replace('montalvo_result_', '')) for _ in data if "montalvo" in _]
    save_counter = max(last)
except:
    save_counter = 0

try:
    with open('parsed_pages.txt') as f:
        lines = [_.strip() for _ in f.readlines()]

except FileNotFoundError:
    f= open("parsed_pages.txt","w+")
    f.close()

for i in range(1, 82321):
    url = f"https://www.montalvospirits.com/page/{i}/"
    if url not in lines:
        get_links(i)
        lines_to_add.append(url)