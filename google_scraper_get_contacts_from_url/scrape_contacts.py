import csv
import requests
import re
import itertools

from typing import List
from bs4 import BeautifulSoup

class ScrapeWebsite():

    def __init__(self,url):
        '''Initialize website scraper variables.'''
        self.result: List = []
        self.base_url: str = url

        #Regex to match cases
        self.number_regex = r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))" #best one
        self.email_regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z0-9]{2,3}" # best one

    def fetch(self, link):
        try:
            response = requests.get(link)
        except:
            print('Request denied:', link)

        return response

    def parse_data_child(self, child_link):
        '''Parsing data if there is contact page.'''
        print('scraping:', child_link)

        child_dict = {}

        #Crawling data in contact url
        request_content = self.fetch(child_link)
        contact_content = BeautifulSoup(request_content.text, 'lxml')

        #Extacting contact data
        emails_contact = list(set(re.findall(self.email_regex, contact_content.get_text())))
        phones_contact = list(set(re.findall(self.number_regex, contact_content.get_text())))

        child_dict['Contact url'] = child_link
        child_dict['Emails (Contact Page)'] = ', '.join(emails_contact) if emails_contact else ''
        child_dict['Phones (Contact Page)'] = ', '.join(phones_contact) if phones_contact else ''

        return child_dict


    def parse_data_parent(self, response):
        '''Parsing base url for possible contacts.'''
        print('scraping:',response.url)

        #Parsing the response
        content = BeautifulSoup(response.text, features = "lxml")

        #Extracting contact data
        emails_home = list(set(re.findall(self.email_regex, content.get_text())))
        phones_home = list(set(re.findall(self.number_regex, content.get_text())))

        parent_dict = {
            'Emails (Homepage)': ', '.join(emails_home) if emails_home else '',
            'Phones (Homepage)': ', '.join(phones_home) if phones_home else '',
            'Emails (Contact Page)': '',
            'Phones (Contact Page)': '',
            'Home url': response.url,
            'Contact url': ''
        }

        #Extracting contacts from contacts page
        try:
            contact_page = content.find('a', text = re.compile('contact', re.IGNORECASE))['href']
            contact_url = contact_page if 'http' in contact_page else response.url[:-1] + contact_page

            #Storing values to dictionary
            child_dict = self.parse_data_child(contact_url)
            parent_dict = dict(parent_dict,**child_dict)
    
        except Exception as e:
            pass

        parent_dict['Status'] = bool(dict(itertools.isslice(parent_dict.items(),4)))


        return parent_dict


    def concat_keyword(self,keyword):
        '''Concat the keyword.
        hey how are you -> hey-how-are-you-jobs
        '''
        data = keyword.split()
        res_key = ""

        for val in data:
            if val == data[-1]:
                res_key += (val+'-jobs')
            else:
                res_key += (val+'-')
        
        return res_key

    def write_csv(self,):
        print('Saving to csv....')

        if self.result: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)
        print("Saved to results.xlsx")


    def run(self,):

        #FETCH DATA
        response = self.fetch(self.base_url)

        #Parse Response
        contacts = self.parse_data_parent(response)

        return contacts


if __name__ == '__main__':
    # try_link = 'https://www.organics.ph/'
    test_link = 'https://www.nytimes.com/'

    scraper = ScrapeWebsite(test_link)

    test = scraper.run()