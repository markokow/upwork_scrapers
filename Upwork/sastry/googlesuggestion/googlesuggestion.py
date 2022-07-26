import requests
from typing import List
import concurrent.futures
import pandas as pd
import itertools
import requests
import string
import json
import time
import datetime


class GoogleSuggestion:
    def __init__(self, *,keywords: List = []) -> None:
        '''Initialize variables used for scraping.'''
        self.keywords: List = keywords
        self.resultList: List = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
        }
        self.charList = " " + string.ascii_lowercase + string.digits
        self.MAX_WORKERS = 20
        self.csv_headers = [None]
        self.today = str(datetime.datetime.now()).split('.')[0].replace('-', '_').replace(':', '_').replace(' ', '_')


    def makeGoogleRequest(self, query):
        # If you make requests too quickly, you may be blocked by google 
        time.sleep(0.1)
        URL="http://suggestqueries.google.com/complete/search"
        PARAMS = {"client":"firefox",
                "hl":'en',
                "q":query}
        headers = {'User-agent':'Mozilla/5.0'}
        response = requests.get(URL, params=PARAMS, headers=headers)
        if response.status_code != 200:
            return "ERR"
        suggestedSearches = json.loads(response.content.decode('utf-8'))[1]
        return suggestedSearches

    def getGoogleSuggests(self,keyword):
        # err_count1 = 0
        queryList = [keyword + " " + char for char in self.charList]
        suggestions = []
        for query in queryList:
            suggestion = self.makeGoogleRequest(query)
            if suggestion != 'ERR':
                suggestions.append(suggestion)

        # Remove empty suggestions
        suggestions = set(itertools.chain(*suggestions))
        if "" in suggestions:
            suggestions.remove("")

        return suggestions

    
    def run(self):
        '''Run all cases using the urls'''
        print("Scraping is running please don't exit...")
        # self.keywords = [f"is * {_} a good place to live" for _ in self.keywords]
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            futuresGoogle = {executor.submit(self.getGoogleSuggests, keyword): keyword for keyword in self.keywords}
            for result, future in enumerate(concurrent.futures.as_completed(futuresGoogle), start=1):
                key = futuresGoogle[future]
                for suggestion in future.result():
                    print(f"found \"{suggestion}\" for key: \"{key}\"")
                    self.resultList.append([key, suggestion])

                outputDf = pd.DataFrame(self.resultList, columns=['Keyword','Suggestion'])
                outputDf.to_csv(f'{self.today}_result_{result}.csv', index=False)

                self.resultList = []


if __name__ == '__main__':
    '''Run main file.'''
    file =  open('inputs.txt', 'r', encoding='utf-8')
    keywords: List = [acc.strip() for acc in file.readlines()]
    #Run scraper
    scraper = GoogleSuggestion(keywords= keywords)
    scraper.run()
