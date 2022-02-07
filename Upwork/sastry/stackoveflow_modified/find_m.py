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

content = BeautifulSoup(response, 'lxml')

print(content)