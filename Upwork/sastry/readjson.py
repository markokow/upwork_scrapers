import json

with open('data.json') as f:
  data = json.load(f)


# print(data)

# print(type(data))
# data = json.dumps(data)

# print(data)
      
# # Serializing json  
# json_object = json.dumps(data, indent = 1) 
# # print(json_object)


# print(type(json_object))


# data = json.dumps(json_object.decode('utf-8'))
# json_data = json.loads(data)
# data2 = json.loads(json_data)

# with open('cleaned.json', 'w', encoding='utf-8') as f:
#     json.dump(data2, f)



for key in data.keys():

    print(key)


questions = data['organic_results']

for question in questions:
#     print(question['query'])
#     print(question['link'])
#     print(question['snippet'])
    # print(question['query'])
    print(question)