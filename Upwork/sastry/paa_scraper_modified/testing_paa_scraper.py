import re
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import io 
import requests_html
from bs4 import BeautifulSoup

def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def fetch_query(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q="+query+"?")

    return response

# def start_program():

def parse_response(response: requests_html.HTMLResponse = None):

    content = BeautifulSoup(response.content, 'lxml', from_encoding="utf-8")

    answer = content.find("div", {"class": "V3FYCf"})
    heading = answer.find("div", {"role":"heading"})

    ppl_also_ask = content.find("div", {"jsname": "N760b"})

    if ppl_also_ask:
        all_paas = ppl_also_ask.find_all("div", {"jsname": "Cpkphb"})

        for paa in all_paas:

            data = paa.find("div", {"jsname": "F79BRe"})
            print(data["data-q"])



def store_response(response, query_name):
    '''Saved response as html.'''
    # if response.status_code == 200:
    print('Saving response as html')
    filename = query_name + ".html"
    with io.open(filename, 'w', encoding = 'utf-8') as html_file:
        html_file.write(response.text)
        print('Done')

# query = "Low maintenance balcony plants"    
# query = "Best potted plants for shaded porch"    
query = "Balcony plants for beginners"    

response = fetch_query(query = query)
parse_response(response = response) 
# store_response(response = response, query_name = query)

