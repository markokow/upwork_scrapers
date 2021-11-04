import os
import json
from datetime import datetime
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
import shutil

# os.system("pip install instagram-scraper")
account: str = 'fritzhansen'


os.system(f"instagram-scraper {account} -u rexvon.apaap@gmail.com -p Bryitkids92073 --media-metadata --include-location --profile-metadata -m 1")

file = open(f'{account}/{account}.json', encoding='utf-8')

data = json.load(file)

posts = data['GraphImages']

result: list = []
result.append(['post_date','media_url','caption','comment_count','number_of_likes'])

for dat in posts:

    _timestamp = dat['taken_at_timestamp']
    _post_date = datetime.utcfromtimestamp(_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    _media_url = dat['display_url']
    _comment_count = dat['edge_media_to_comment']['count']
    _number_of_likes = dat['edge_media_preview_like']['count']
    _caption = dat['edge_media_to_caption']['edges'][0]['node']['text']

    result.append([_post_date,_media_url,_caption,_comment_count,_number_of_likes])
        
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'dev-monolith-331102-d5754db1b0f8.json'

credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '17kopo5eo2-Xmw27yItjvv3J3S-V0CwzA2hseqy_LUPc'
SAMPLE_RANGE_NAME = 'IG1!A1'

service = build('sheets', 'v4', credentials=credentials)

# Call the Sheets API
sheet = service.spreadsheets()

result = service.spreadsheets().values().update(
    spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
    valueInputOption="USER_ENTERED", body={"values": result}).execute()

print(result)

shutil.rmtree(f'{account}')
print("Successfully deleted folder and all of its contents.")

