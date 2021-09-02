import requests
import urllib
from typing import List
from bs4 import BeautifulSoup
import shutil

site_map = 'https://www.pngmart.com/sitemap.xml/'

site_req = requests.get(site_map)

soup = BeautifulSoup(site_req.text, 'lxml')

site_map = soup.find_all('loc')

# site_list:List[str] = []
master_list: List[str] = []
image_list: List[str] = []


def parse_then_download_img(url):
    site_req = requests.get(url, stream=True, allow_redirects=True)
    soup = BeautifulSoup(site_req.text, 'lxml')
    img_url = soup.find('a', class_ = 'download')['href']

    img_title = f"{url.split('/')[-1]}_{img_url.split('/')[-1]}"

    print(img_url)

    urllib.request.urlretrieve(img_url, img_title)
    # with open(img_title, 'wb') as file:
    #     # site_req.raw.decode_content = True
    #     shutil.copyfileobj(site_req.raw, file)
    #     # file.write(site_req.content)
    print('saved', img_title)

    del site_req
    return img_url




def get_post_list(site_url):
    site_req = requests.get(site_url)
    soup = BeautifulSoup(site_req.text, 'lxml')
    site_map = soup.find_all('loc')

    
    site_list:List[str] = []


    for site in site_map:
        site_url = site.text
        if 'image' in site_url:
            img_url = parse_then_download_img(site_url)
            site_list.append(img_url)
            # print("adding", img_url)





    return site_list


for site in site_map:
    site_url = site.text
    try:
        if 'sitemap_post' in site_url and 'tag' not in site_url: 
            # site_list.append(site_url)
            master_list.extend(get_post_list(site_url))
    except Exception as e:
        print(e)







# get_post_list(site_list[1])