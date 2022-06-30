# Pemavor.com Autocomplete Scraper
# Author: Stefan Neefischer (stefan.neefischer@gmail.com)

import concurrent.futures
import pandas as pd
import itertools
import requests
import string
import json
import time

startTime = time.time()

# If you use more than 50 seed keywords you should slow down your requests - otherwise google is blocking the script
# If you have thousands of seed keywords use e.g. WAIT_TIME = 1 and MAX_WORKERS = 10

WAIT_TIME = 0.1
MAX_WORKERS = 20

# set the autocomplete language
lang = "en"

charList = " " + string.ascii_lowercase + string.digits

def makeGoogleRequest(query):
    # If you make requests too quickly, you may be blocked by google 
    time.sleep(WAIT_TIME)
    URL="http://suggestqueries.google.com/complete/search"
    PARAMS = {"client":"firefox",
            "hl":lang,
            "q":query}
    headers = {'User-agent':'Mozilla/5.0'}
    response = requests.get(URL, params=PARAMS, headers=headers)
    if response.status_code != 200:
        return "ERR"
    suggestedSearches = json.loads(response.content.decode('utf-8'))[1]
    return suggestedSearches

def getGoogleSuggests(keyword):
    # err_count1 = 0
    queryList = [keyword + " " + char for char in charList]
    suggestions = []
    for query in queryList:
        suggestion = makeGoogleRequest(query)
        if suggestion != 'ERR':
            suggestions.append(suggestion)

    # Remove empty suggestions
    suggestions = set(itertools.chain(*suggestions))
    if "" in suggestions:
        suggestions.remove("")

    return suggestions

#read your csv file that contain keywords that you want to send to google autocomplete
# df = pd.read_csv("keyword_seeds.csv")
# Take values of first column as keywords
# keywords = df.iloc[:,0].tolist()
keywords = ["is * texas a good place to live"]

resultList = []

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futuresGoogle = {executor.submit(getGoogleSuggests, keyword): keyword for keyword in keywords}

    for future in concurrent.futures.as_completed(futuresGoogle):
        key = futuresGoogle[future]
        for suggestion in future.result():
            resultList.append([key, suggestion])

    # Convert the results to a dataframe
    outputDf = pd.DataFrame(resultList, columns=['Keyword','Suggestion'])

# Save dataframe as a CSV file
outputDf.to_csv('keyword_suggestions.csv', index=False)
print('keyword_suggestions.csv File Saved')

print(f"Execution time: { ( time.time() - startTime ) :.2f} sec")