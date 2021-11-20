import os
import zipfile
try:
    import lzma
except ImportError:
    from backports import lzma

import json




archive = lzma.open('ethnicraft/2021-11-18_19-01-49_UTC.json.xz').read()


data = json.dumps(archive.decode('utf-8'))

# print(data)

json_data = json.loads(data)
data2 = json.loads(json_data)

post_date = data2['node']['taken_at_timestamp']
media_url = data2['node']['thumbnail_src']
number_of_comments = data2['node']['edge_media_to_comment']['count']
number_of_likes = data2['node']['edge_liked_by']['count']
caption = data2['node']['edge_media_to_caption']['edges'][0]['node']['text']

print(post_date)
print(media_url)
print(number_of_comments)
print(number_of_likes)
print(caption)


with open('data.json', 'w', encoding = 'utf-8') as f:
    json.dump(data2, f, ensure_ascii=False, indent = 4)

# print(type(json_data))
# print(type(data))
# account = 'ethnicraft'

# os.system(f"instaloader --fast-update profile {account} --geotags")

# my_list = os.listdir(account)

# all_json = [val for val in my_list if val.endswith('json.xz')]

# # archive = zipfile.ZipFile([all_json[-2],'r'])
# archive = zipfile.ZipFile('ethnicraft/2021-11-18_19-01-49_UTC.json.xz','r')

# print(type(archive))
# jsonFile = archive.open(all_json[-2][:-3])

# # for val in all_json:

# #     print(val)

# print(jsonFile)



