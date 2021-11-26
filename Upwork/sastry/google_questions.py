from serpapi import GoogleSearch
import json

params = {
  "q": "plants to grow in balcony",
  "api_key": "8a1844cbed6362cae3d6398fa5db5f11a03cd6b160758b94dd26c633667bbc60"
}

search = GoogleSearch(params)
results = search.get_dict()
# related_questions = results['related_questions']


with open('data.json', 'w') as f:
    json.dump(results, f)


