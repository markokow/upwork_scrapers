import requests
import json
from pprint import pprint
r=requests.get("https://www.google.com/maps/search/restaurant+in+washington+dc/@38.9002851,-77.041265,14z/data=!3m1!4b1")

txt = r.text

find1 = "window.APP_INITIALIZATION_STATE="
find2 = ";window.APP"

i1 = txt.find(find1)
i2 = txt.find(find2, i1+1 )
js = txt[i1+len(find1):i2]
data = json.loads(js)

count = 0
for dat in data:

    print(dat)
    break