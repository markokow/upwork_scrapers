import csv
import requests
import re
from bs4 import BeautifulSoup

class ScrapeWebsite():

    def __init__(self,url):

        self.result = []
        self.base_url = url

        


        # self.number_regex = r"(\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*(\d{1,2})$)"
        # self.number_regex = r"(\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*(\d{1,2})$)"
        # self.number_regex = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
        self.number_regex = r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))" #best one
        # self.number_regex = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
        # self.number_regex = r"((?:\d{3}|\(\d{3}\))?(?:\s|-|\.)?\d{3}(?:\s|-|\.)\d{4})"
        self.email_regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z0-9]{2,3}" # best one
        # self.email_regex = r"[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,64}"
        # self.email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    def fetch(self, link):
        try:
            response = requests.get(link)
        except:
            print('Request denied.')

        return response

    def parse_data_child(self, child_link):
        print('scraping', child_link)

        child_dict = {}

        #Crawling data in contact url
        request_content = self.fetch(child_link)
        contact_content = BeautifulSoup(request_content.text, 'lxml')

        print('hey')
        mail_test = contact_content.find_all('a')
        print(mail_test)
        for x in mail_test:
            print(x.get('href'))
        
        #Extacting contact data
        emails_contact = list(set(re.findall(self.number_regex, contact_content.get_text())))
        phones_contact = list(set(re.findall(self.email_regex, contact_content.get_text())))

        child_dict['Emails (Contact Page)'] = ', '.join(emails_contact) if emails_contact else ''
        child_dict['Phones (Contact Page)'] = ', '.join(phones_contact) if phones_contact else ''

        return child_dict


    def parse_data_parent(self, response):

        print('scraping',response.url)

        #Parsing the response
        content = BeautifulSoup(response.text, features = "lxml")

        #Extracting contact data
        emails_home = list(set(re.findall(self.number_regex, content.get_text())))
        phones_home = list(set(re.findall(self.email_regex, content.get_text())))

        parent_dict = {
            'Emails (Homepage)': ', '.join(emails_home) if emails_home else '',
            'Phones (Homepage)': ', '.join(phones_home) if phones_home else '',
            'Emails (Contact Page)': '',
            'Phones (Contact Page)': ''
        }

        #Extracting contacts from contacts page
        try:
            contact_page = content.find('a', text = re.compile('contact', re.IGNORECASE))['href']

            contact_url = contact_page if 'http' in contact_page else response.url[:-1] + contact_page

            child_dict = self.parse_data_child(contact_url)

            parent_dict = dict(parent_dict,**child_dict)
    
        except Exception as e:
            pass



        return parent_dict


    def concat_keyword(self,keyword):
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
    try_link = 'https://play.afl/club-finder'

    scraper = ScrapeWebsite(try_link)

    test = scraper.run()

    print(test)