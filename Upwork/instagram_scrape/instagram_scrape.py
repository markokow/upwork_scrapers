# from keep_alive import keep_alive
import os
import json
from datetime import datetime
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
import shutil
import time
import re

file = open('ig_users.txt', 'r')
accounts = [acc.strip() for acc in file.readlines()]

file = open('google_sheets_id.txt', 'r')
links = [
    re.search("spreadsheets/d/(.*)/edit", acc.strip()).group(1)
    for acc in file.readlines()
]

my_secret_user = 'jamesscaifeupwork2@gmail.com'
my_secret_pass = 'upwork2021&'

while True:

  try:

    os.system(
        f"instagram-scraper -f ig_users.txt -u {my_secret_user} -p {my_secret_pass} --retry-forever --media-type image video --media-metadata -i --include-location --profile-metadata -m 1 --cookiejar cookies.txt"
    )

    for account, link in zip(accounts, links):

        file = open(f'{account}/{account}.json', encoding='utf-8')

        data = json.load(file)

        try:

            posts = data['GraphImages']

            # If modifying these scopes, delete the file token.json.
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            SERVICE_ACCOUNT_FILE = 'dev-monolith-331102-d5754db1b0f8.json'

            credentials = None
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)

            # The ID and range of a sample spreadsheet.
            SAMPLE_SPREADSHEET_ID = link
            SAMPLE_RANGE_NAME = 'Sheet1!A1'

            service = build('sheets', 'v4', credentials=credentials)

            # Call the Sheets API
            sheet = service.spreadsheets()

            result: list = []
            result.append([
                'post_date', 'media_url', 'caption', 'comment_count',
                'number_of_likes'
            ])

            #Pull data from spreadsheetId
            sheet_result = sheet.values().get(spreadsheetId = SAMPLE_SPREADSHEET_ID, range = 'Sheet1!A:E').execute()

            values = sheet_result.get('values', [])[1:]

            result = result + values

            for dat in posts:

                _timestamp = dat['taken_at_timestamp']
                _post_date = datetime.utcfromtimestamp(_timestamp).strftime(
                    '%Y-%m-%d %H:%M:%S')
                _media_url = dat['display_url']
                _comment_count = dat['edge_media_to_comment']['count']
                _number_of_likes = dat['edge_media_preview_like']['count']
                _caption = dat['edge_media_to_caption']['edges'][0]['node'][
                    'text']

                if _media_url != result[-1][1]:
                  result.append([
                      _post_date, _media_url, _caption, _comment_count,
                      _number_of_likes
                  ])

            sheet_result = service.spreadsheets().values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=SAMPLE_RANGE_NAME,
                valueInputOption="USER_ENTERED",
                body={
                    "values": result
                }).execute()

            print(sheet_result)

        except KeyError:
            print(f"Skipping {account}. Will reupdate in 24 hours.")

        finally:
            shutil.rmtree(f'{account}')
            print(
                f"Successfully deleted \"{account}\" folder and all of its contents."
            )

    print("All instagram accounts pulled. Resetting in 24 hours.")
    time.sleep(86400)

  except FileNotFoundError:
    print("Refreshing in 10 minutes.")
    time.sleep(600)
    continue
