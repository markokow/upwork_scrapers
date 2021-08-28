
from bs4 import BeautifulSoup
import requests


URL = 'https://crs.upd.edu.ph/'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
'origin': URL, 'referer': 'https://www.google.com/'}

s = requests.Session()

# print(s.status_code)
csrf_token = s.get(URL).cookies['crs_csrf_token']

login_payload = {
    'login': 'raapaap',
    'password': 'bryitkids'
}

log_req = s.post(URL, headers = HEADERS, data = login_payload)

cookies = log_req.cookies

soup = BeautifulSoup(s.get(URL + '/user/view/classmessages').text, 'html.parser')

print(soup.find('em', class_ = 'paid'))



