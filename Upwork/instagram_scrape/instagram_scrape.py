import os
import json
import pandas as pd
from datetime import datetime
import csv

result: list = []

# os.system("pip install instagram-scraper")
account: str = 'kevin'

# os.system(f"instagram-scraper {account} -u rexvon.apaap@gmail.com -p Bryitkids92073 --media-metadata --include-location --profile-metadata -m 10")

file = open(f'{account}/{account}.json', encoding='utf-8')

data = json.load(file)

posts = data['GraphImages']


result.append(['post_date','media_url','caption','comment_count','number_of_likes'])

# counter = 1

for dat in posts:

    _timestamp = dat['taken_at_timestamp']
    _post_date = datetime.utcfromtimestamp(_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    _media_url = dat['display_url']
    _comment_count = dat['edge_media_to_comment']['count']
    _number_of_likes = dat['edge_media_preview_like']['count']
    _caption = dat['edge_media_to_caption']['edges'][0]['node']['text']

    result.append([_post_date,_media_url,_caption,_comment_count,_number_of_likes])

    # _features = {
    #     'post_date': _post_date,
    #     'media_url': _media_url,
    #     'caption': _caption,
    #     'comment count': _comment_count,
    #     'number of likes': _number_of_likes,
    # }

    # result.append(_features)

def _write_csv(result: list = []):
    '''Save results to csv.'''
    print('Saving to csv....')

    if result: 
        with open(f'{account}.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
            writer_object = csv.DictWriter(csv_file, fieldnames = result[0].keys())
            writer_object.writeheader()

            for row in result:
                writer_object.writerow(row)
        print("Saved to results.xlsx")
    
    else:
        print('No data was saved')
        

# _write_csv(result = result)

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'intense-talent-327208-2edab6a7d6ae.json'

credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1nciStQYv5ryCxrkKx5APFWOmJk1_MMudynGE6VJTzg4'
SAMPLE_RANGE_NAME = 'data!A1'

service = build('sheets', 'v4', credentials=credentials)

# Call the Sheets API
sheet = service.spreadsheets()

test = [["hey", "hi"],[1,2]]

result = service.spreadsheets().values().update(
    spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
    valueInputOption="USER_ENTERED", body={"values": result}).execute()
