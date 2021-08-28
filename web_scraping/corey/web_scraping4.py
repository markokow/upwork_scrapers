from bs4 import BeautifulSoup
import requests
from requests.api import head
 
source = requests.get('https://coreyms.com/').text
soup = BeautifulSoup(source, 'lxml')

article = soup.find('article')
# headline = article.h2.text
# print(headline)

vid_src = article.find('iframe', class_ = 'youtube-player')['height']
print(type(vid_src))
