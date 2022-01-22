
import json
from TikTokApi import TikTokApi
import pandas as pd
from typing import List
import string


verifyFp='A901ADD17B05AA0F3DEE3E324969875F~k3Il5Ym9lla3pCXfWqumMGfAMifpFQjIg6xQrLpBcL96uiCktzIFMXxYur1Jq3M2P8SuxaDNhwDvivFeQRkPXRXFc0GOZ0gR4BvsF9/PsdwC2Yb/+x99GAlYhU17Pyzlsab2b0LPQpTRG1BcXBRj/OIs6QorKNOrKKWfZNmNEoQ='
tt_wev = '7Cbf4243546e874e40c6497d0e0fb20292afce4cd4515ac4fe05f523381492a776'

cookie = {
  "s_v_web_id": "<your_key>",
  "tt_webid": tt_wev
}

api = TikTokApi.get_instance(use_test_endpoints=True, cookie=cookie)
results = 100000
hashtag = '#partnership'
search_results = api.by_hashtag(count=results, hashtag=hashtag)


jsonString = json.dumps(search_results, indent = 2)

with open('json_data.json', 'w') as outfile:
    outfile.write(jsonString)

print(search_results)
print(type(search_results))


printable = set(string.printable)

def remove_spec_chars(in_str):
    return ''.join([c for c in in_str if c in printable])

result: List = []
for tiktok in search_results:
    feature: dict = {}

    feature['video_url'] = tiktok['video']['playAddr']
    feature['author_id'] = tiktok['author']['id']
    feature['author_nickname'] = tiktok['author']['nickname']
    feature['author_unique'] = tiktok['author']['uniqueId']
    feature['music'] = tiktok['music']['playUrl']
    feature['caption'] = tiktok['desc'].strip()

    result.append(feature)

df = pd.DataFrame(result)

df['caption'] = df['caption'].apply(remove_spec_chars)

df.to_csv('sponsored.csv', index=False, encoding='utf-8')