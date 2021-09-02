import csv
from typing import List
import requests
from bs4 import BeautifulSoup


class gia_report():

    def __init__(self,):

        self._target_url: List[str] = []
        self._result: List[dict] = []


    def write_csv(self,):

        _dict: dict = {}

        for val in self._result:
            _dict = {**_dict,**val}
        '''Save results to csv.'''

        print('saving to csv....')

        if self._result: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = _dict.keys())
                writer_object.writeheader()

                for row in self._result:
                    writer_object.writerow(row)
            print("saved to results.csv")
        
        else:
            print('no data was saved')

    def _load_csv(self,):

        print('opening target.csv')
        try:
            with open('target.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self._target_url.append(row[0])
        except Exception as e:
            print(e)
            pass


    def _fetch_site(self, url):

        response = requests.get(url)

        return response


    def _parse_data(self,response):

        _content = BeautifulSoup(response.content, 'lxml')

        _iframes = _content.find_all('iframe')

        print(_iframes)

        # for x in _iframes:

        #     print(x)
            # print(x.get_attribute('src'))



    def _run(self,):

        self._load_csv()

        for _url in self._target_url:

            print(_url)

            _resp = self._fetch_site(_url)
            self._parse_data(_resp)
            break

            

        # print(self._target_url)

        # for _path in self._paths:
        #     # print(_path)
        #     self._read_json(_path)

        #     #restart _dat_dict
        #     self._dat_dict = {}

        #     self._parse_dict(self._data)

        #     value = {k: v for k,v in self._dat_dict.items() if v}
        #     self._result.append(value)

        # self.write_csv()



if __name__ == '__main__':

    scrape =gia_report()

    scrape._run()
