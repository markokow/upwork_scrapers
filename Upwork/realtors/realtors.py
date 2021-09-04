import requests
import requests.exceptions
import csv
import json
import re
from bs4 import BeautifulSoup
from typing import List

class Coaches():

    def __init__(self):

        self.base_url = 'http://www.ggar.com/index.php?src=directory&view=rets_agents&srctype=rets_agents_lister&query=&xsearch_id=rets_agents_search&xsearch[0]=&xsearch[1]=&pos=0,20,4652'

        self.result: List[dict] = []
        self.inputs: List[dict] = []
        self.email_regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z0-9]{2,64}" # best one


    def fetch(self, link):
        try:
            response = requests.get(link)
        except:
            raise Exception

        return response

    def _parse(self,response):


 
        _cont = BeautifulSoup(response.text, 'lxml')

 

        _retsList = _cont.find('table', class_ = 'retsList')
        

        _trs = _retsList.find_all('tr')

        for _tr in _trs[1:]:

            _data_dict: dict = {}

            _a = _tr.find('a', href = True)
            _td = _tr.find_all('td')


            _name = _a.text
            _company_name = _td[1].text
            _phone_number = _td[-1].text


            _data_dict['Name - Company Name'] = '{} - {}'.format(_name, _company_name)
            _data_dict['Phone Nunber'] = _phone_number

            _url = 'http://www.ggar.com/' + _a['href']

            _child_resp = self.fetch(_url)
            _child_cont =  BeautifulSoup(_child_resp.text, 'lxml')


            _cont_tab = _child_cont.find('table', class_ = 'contactInfo')
            _a = _cont_tab.find('a', href = True)

            _script = _cont_tab.find('script').string

            _vals = re.findall(r"'\w+'",_script)

            _vals = [x.replace("'", '') for x in _vals]
            _email = '{}@{}.{}'.format(_vals[0],_vals[1],_vals[-1])

            _data_dict['Email'] = _email

            self.result.append(_data_dict)


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

        _resp = self.fetch(self.base_url)
        self._parse(_resp)

        print(self.result)
        self.write_csv()


if __name__ == '__main__':
    # try_link = 'https://www.organics.ph/'
    # try_link = 'https://www.vq.org.au/play-learn/find-club/?postcode'

    scraper = Coaches()

    scraper.run()