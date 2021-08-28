import re
import requests
import requests.exceptions
import csv
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup

class ScrapeWebsite():

    def __init__(self,url):

        self.base_url = url

        self.unprocessed_urls = deque([url])
        self.processed_urls = set()

        #Dictionary containing emails and numbers
        self.result = []

        self.emails = set()
        self.numbers = set()

        #Regex for emails and number
        # self.number_regex = r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{}))" #best one
        self.number_regex = r"^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$"
        # r"\^[\\(]{0,1}([0-9]){3}[\\)]{0,1}[ ]?([^0-1]){1}([0-9]){2}[ ]?[-]?[ ]?([0-9]){4}[ ]*((x){0,1}([0-9]){1,5}){0,1}",
        # r"^[2-9]\d{2}-\d{3}-\d{4}$", 
        # r"((\(\d{3}\) ?)|(\d{3}-))?\d{3}-\d{4}",
        # r"\(([0-9]{2}|0{1}((x|[0-9]){2}[0-9]{2}))\)\s*[0-9]{3,4}[- ]*[0-9]{4}") #trial
        self.email_regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z0-9]{1,7}" # best one

        #Block parse emails that end with this
        self.blocked_email: tuple = ('png')

    def fetch(self, link):
        try:
            response = requests.get(link)
        except:
            raise Exception

        return response

    def clean_and_update(self,new_emails, new_number):

        for x,y in zip(new_emails, new_number):
            print(x,y)
            x = x.strip()
            y = y.strip(
            )
        
        #Updates emails and numbers
        self.emails.update(new_emails)
        self.numbers.update(new_number)

        #Filter those parsed emails that ends with elements in self.blocked_emails
        self.emails = set(filter(lambda x: not x.endswith(self.blocked_email), list(self.emails)))
        
    def parse_contacts(self, response):

        print('scraping',response.url)

        contact_content = BeautifulSoup(response.text, 'lxml')


        #Finding emails and numbers in the response
        new_emails = set(re.findall(self.email_regex, response.text, re.I))
        # new_number = set(re.findall(r"^[\\(]{0,1}([0-9]){3}[\\)]{0,1}[ ]?([^0-1]){1}([0-9]){2}[ ]?[-]?[ ]?([0-9]){4}[ ]*((x){0,1}([0-9]){1,5}){0,1}", response.text, re.I))

        # new_emails = set(re.findall(self.email_regex, contact_content.get_text()))
        new_numbers = (set(re.findall(self.number_regex, contact_content.get_text())))

        #Update the class set
        self.clean_and_update(new_emails, new_numbers)


    def parse_anchors(self,response) -> None:

        # extract base url to resolve relative links
        url = response.url

        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url


        soup = BeautifulSoup(response.text, 'lxml')

        # Once this document is parsed and processed, now find and process all the anchors i.e. linked urls in this document
        for anchor in soup.find_all("a"):
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            # resolve relative links (starting with /)
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            # add the new url to the queue if it was not in unprocessed list nor in processed list yet
            if not link in self.unprocessed_urls and not link in self.processed_urls:
                self.unprocessed_urls.append(link)


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

        count = 0
        while (self.unprocessed_urls):
                count+=1
                if count == 30:
                    break
                # move next url from the queue to the set of processed urls
                url = self.unprocessed_urls.popleft()

                print('scraping', url)

                self.processed_urls.add(url)

                # get url's content
                # print("Crawling URL %s" % url)
                try:
                    response = self.fetch(url)
                # except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                except:
                    # ignore pages with errors and continue with next url
                    continue

                #Call functions to get concurrent links and extract data
                self.parse_anchors(response) 
                self.parse_contacts(response)

        results_dict = {
            'Emails': ', '.join(self.emails),
            'Phone Numbers': ', '.join(self.numbers)
        }

        print(results_dict)


if __name__ == '__main__':
    # try_link = 'https://www.organics.ph/'
    try_link = 'https://www.vq.org.au/play-learn/find-club/?postcode'

    scraper = ScrapeWebsite(try_link)

    scraper.run()