from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
url = 'https://majestic.com/'
req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

webpage = urlopen(req).read()
page_soup = soup(webpage, "html.parser")

print(page_soup)