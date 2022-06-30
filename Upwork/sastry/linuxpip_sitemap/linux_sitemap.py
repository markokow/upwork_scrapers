import requests
from bs4 import BeautifulSoup
from typing import List
from urllib.parse import urlparse

base_map: str = 'https://frameboxxindore.com/sitemap_index.xml'
# base_map: str = 'https://linuxpip.org/sitemap_index.xml'
result: List = []
file_names: List =[]

def fetch(url):
    '''Fetch the url and returns bs4 object.'''
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    response = requests.get(url, headers = headers)

    if response.status_code != 200:
        print(f"Status code: {response.status_code}")
        print("Error! Please exit scraper and wait a few hours.")

    return response

def search_sitemap(url, filename: str = ''):

    if url in result:
        print(f"skipping. {url} already present in existing results.txt")

    else:
        netloc = urlparse(url).netloc
        resp = fetch(url)
        if resp.status_code == 200:
            content = BeautifulSoup(resp.content, 'lxml')
            urls = [_.text.strip() for _ in content.find_all("loc")] 
            if urls:
                this_netloc = urlparse(url).netloc
                if this_netloc == netloc:
                    this_netloc = this_netloc.split('.')[0]
                    filename = url.split('/')[-1].split('.')[0]
                    filename = f"{this_netloc}-{filename}.txt"
                if filename not in file_names:
                    file_names.append(filename)
                for _url in urls:
                    if _url in result:
                        print(f"skipping. {_url} already present in existing results.txt")
                        continue
                    else:
                        search_sitemap(_url, filename)
            else:
                this_netloc = urlparse(url).netloc
                if this_netloc == netloc:
                    print(url)
                    save_to_file(url, filename)
                    save_to_file(url, "results.txt")
                    # result.append(url)
def save_to_file(data, filename):
    textfile = open(filename, "a")
    textfile.write(data + "\n")
    textfile.close()

try:                
    my_file = open("results.txt", "r")
    result = [_.strip() for _ in my_file.readlines()] 
except:
    pass
# ??try:        
search_sitemap(base_map, '')
# except KeyboardInterrupt:
#     textfile = open("results.txt", "w")
#     for element in result:
#         textfile.write(element + "\n")
#     textfile.close()

# textfile = open("results.txt", "w")
# for element in result:
#     textfile.write(element + "\n")
# textfile.close()