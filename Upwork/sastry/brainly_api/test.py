import requests
if __name__ == '__main__':
    API_KEY = '9dbc100070f87da569a02d0e6c609b26'
    URL_TO_SCRAPE = 'https://brainly.com/graphql/us?operationName=feed&variables=%7B%22gradeIds%22:[],%22subjectIds%22:[5],%22statusId%22:%22ALL%22,%22cursor%22:null,%22feedType%22:%22PUBLIC%22,%22first%22:20%7D&extensions=%7B%22persistedQuery%22:%7B%22version%22:1,%22sha256Hash%22:%22a18dcee8ff57280c79a46e830df335650f7c74a60266dceb332a055b8a315b16%22%7D%7D'
    payload = {'api_key': API_KEY, 'url': URL_TO_SCRAPE}
    r = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
    print(r.text)