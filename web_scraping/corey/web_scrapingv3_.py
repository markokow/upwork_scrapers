from bs4 import BeautifulSoup
import requests

with open('home.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')
    print(type(soup))
matches = soup.find_all('div', class_ = 'article')
for match in matches:
    print("****************************************************")
    print(type(match))
    print(match)