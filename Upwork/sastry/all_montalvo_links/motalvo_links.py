import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv
from datetime import datetime


results = []
saved_links = []

main_page = "www.montalvospirits.com"
file_name = str(datetime.today()).replace(':','-')
save_counter: int = 0
max_save: int = 50

def get_links(page_url):
    global pages
    global max_save
    global save_counter
    #   pattern = re.compile("^(/)")
    _headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    }

    proxy = {
        # 'https': 'https://41.217.219.53:31398'
    }
    html = requests.get(page_url, headers=_headers, proxies=proxy) # fstrings require Python 3.6+
    
    if html.status_code == 200:

        not_in_results = []
        soup = BeautifulSoup(html.content, "html.parser")

        for link in soup.find_all("a", href = True):

            data = link["href"]
            netloc = urllib.parse.urlparse(data).netloc

            if (netloc == main_page) | data.startswith("/"):
                if data.startswith("/"):
                    data = urllib.parse.urljoin(page_url, data)

                if data not in results:
                    results.append(data)
                    not_in_results.append(data)
                    print(data)

        to_save = []
        if (len(results) - len(saved_links)) > max_save:
            for dat in results:
                if dat not in saved_links:
                    saved_links.append(dat)
                    to_save.append(dat)
                    if len(dat) == max_save:
                        break

            save_counter += 1
            with open(f'{file_name}_{save_counter}.txt', 'w') as f:
                for item in to_save:
                    f.write("%s\n" % item)

        for link in not_in_results:
            get_links(link)


def write_csv():
        print('Saving to csv....')

        if results: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = results[0].keys())
                writer_object.writeheader()

                for row in results:
                    writer_object.writerow(row)
        print("Saved to test.xlsx")


get_links('https://www.montalvospirits.com/')
        