import requests
import requests.exceptions
import csv

from bs4 import BeautifulSoup
from typing import List

class Coaches():

    def __init__(self):

        self.base_url = 'https://www.thebeachguide.co.uk/beach-list'

        self.result: List[dict] = []
        self.inputs: List[dict] = []


    def fetch(self, link):
        try:
            response = requests.get(link)
        except:
            raise Exception

        return response

    def _parse(self,response):
        
        print('scraping',response.url)

        # print()

        _beaches_content = BeautifulSoup(response.text, 'lxml')

        _beaches = _beaches_content.find_all('a', href=True)
        
        halt = 0
        for _input in self.inputs:

            _url: str = ''

            _item =  _input['\ufeffLocation Name']
            max_count: int = 0

            for _beach in _beaches:

                _beach_name = _beach.text.strip()

                temp_count: int = 0

                if _item ==  _beach_name :
                    _url = 'https://www.thebeachguide.co.uk' + _beach['href']
                    break

                else:
                    _splits = _item.split()
                    for _split in _splits:

                        if _split.lower() in _beach_name.lower():
                            temp_count += 1
                    
                    if temp_count > max_count:
                        max_count = temp_count
                        _url = 'https://www.thebeachguide.co.uk' + _beach['href']

            print(_url)
            _child_resp = self.fetch(_url)
            _child_cont = BeautifulSoup(_child_resp.text, 'lxml')

            _divs = _child_cont.find_all('div', class_ = 'small-6 cell')

            _input['URL'] = _url


            count = 0
            for _div in _divs:
                if count == 0:
                    _p = _div.find_all('p')

                    _input['Type of Beach'] = _p[0].text
                    _input['Lifeguard Service'] = _p[1].text
                    _input['Dogs Friendly Beach?'] = _p[2].text

                    try:
                        _activities = _div.find('ul')
                        _allact = _activities.find_all('li')

                        _actlist = []
                        for _act in _allact:
                            _actlist.append(_act.text)
                        _input['Activities'] = "\n".join(_actlist)
                    except:
                        _input['Activities'] = 'no data'

                    try:
                        _fac = _div.find_all('ul')[-1]
                        _allfac = _fac.find_all('li')
                        _factlist = []

                        for _val in _allfac:
                            _factlist.append(_val.text)
                        _input['Facilities'] = "\n".join(_factlist) 
                    except:
                        _input['Facilities'] = 'no data' 

                else:
                    _p = _div.find_all('p')

                    _input['Nearest Town'] = _p[0].text
                    try:
                        _input['Postcode'] = _p[1].text
                    except:
                        _input['Postcode'] = 'no data'
                    try:
                        _input['OS Grid Ref'] = _p[2].text
                    except:
                        _input['OS Grid Ref'] = _p[-1].text


                    try:
                        _img = _div.find('img')
    
                        _src = _img['src'].split('/')[-1].replace('star.gif', ' star')

                        if 'star' not in _src:
                            _input['Water Quality'] = 'no data'
                        else:
                            _input['Water Quality'] = _src

                    except:
                        _input['Water Quality'] = 'no data'
                    break
                count+=1

            print(_input)
            self.result.append(_input)


    def write_csv(self,):
        print('Saving to csv....')

        if self.result: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)
        print("Saved to results.xlsx")


    def load_input(self,):
        try:
            with open('244 Beaches.csv', 'r', newline = '',encoding = 'utf-8') as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:

                    self.inputs.append(row)
        except:
            print('CSV does not exit')

    def run(self,):

        _resp = self.fetch(self.base_url)

        self.load_input()
        self._parse(_resp)
        # print(self)
        self.write_csv()


if __name__ == '__main__':
    # try_link = 'https://www.organics.ph/'
    # try_link = 'https://www.vq.org.au/play-learn/find-club/?postcode'

    scraper = Coaches()

    scraper.run()