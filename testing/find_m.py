import csv
import requests
import io
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime

headers = {
            'User-Agent': 'Mozilla/5.0',
        }

response = requests.get("https://kidadl.com/articles/best-japanese-names-that-start-with-m", headers = headers)

# print(response.status_code)
content = BeautifulSoup(response.content, 'lxml')

m_letters = [x.text.strip() for x in content.find_all("strong") if len(x.text.strip()) == 5]

print(m_letters)
