import re
# import typing
import requests
import requests.exceptions
import csv
# from urllib.parse import urlsplit
# from collections import deque
from bs4 import BeautifulSoup
from typing import List

class Coaches():

    def __init__(self):

        self.base_url = 'https://www.pro-football-reference.com/coaches/'

        self.result: List[dict] = []


    def fetch(self, link):
        try:
            response = requests.get(link)
        except:
            raise Exception

        return response

    def _parse_coach(self, response):

        _data_dict: dict = {}

        _coach_content = BeautifulSoup(response.text, 'lxml')
    
        _name = _coach_content.find('h1', {'itemprop': 'name'}).text.strip()

        _table = _coach_content.find('table', {'id':'coaching_results'})

        # print(_table.text)
        count = 0

        if _table.find_all('td',{'data-stat':'team'})[-1].text.strip() == ' ':
            _currteam = _table.find_all('td',{'data-stat':'team'})[-2].text.strip()
            _overallwin = _table.find_all('td',{'data-stat':'wins'})[-1].text.strip()
            _overallloss = _table.find_all('td',{'data-stat':'losses'})[-1].text.strip()
            _overalltie = _table.find_all('td',{'data-stat':'ties'})[-1].text.strip()
            _currentwin = _overallwin
            _currentloss = _overallloss
            _currenttie = _overalltie
        
        else:
            for _team in _table.find_all('td',{'data-stat':'team'}):
                if _team.text.strip() == '':
                    _overallwin = _table.find_all('td',{'data-stat':'wins'})[count].text.strip()
                    _overallloss = _table.find_all('td',{'data-stat':'losses'})[count].text.strip()
                    _overalltie = _table.find_all('td',{'data-stat':'ties'})[count].text.strip()
                    break
                else:
                    count += 1
                    continue
            
            _currteam = _table.find_all('td',{'data-stat':'team'})[-2].text.strip()
            _currentwin = _table.find_all('td',{'data-stat':'wins'})[-1].text.strip()
            _currentloss = _table.find_all('td',{'data-stat':'losses'})[-1].text.strip()
            _currenttie = _table.find_all('td',{'data-stat':'ties'})[-1].text.strip()


        _data_dict['Coach Name'] =  _name
        _data_dict['Current Team'] =  _currteam
        _data_dict['Overall Win'] =  _overallwin
        _data_dict['Overall Loss'] =  _overallloss
        _data_dict['Overall Tie'] =  _overalltie
        _data_dict['Current Win'] =  _currentwin
        _data_dict['Current Loss'] =  _currentloss
        _data_dict['Current Tie'] =  _currenttie

        print(_data_dict)

        self.result.append(_data_dict)
        # _coach

    def _parse(self,response):
        
        print('scraping',response.url)

        _coaches_content = BeautifulSoup(response.text, 'lxml')
        _names = _coaches_content.find_all('td', {'data-stat':'coach'})

        count = 0
        for _name in _names:
            if count == 10:
                break
            _a = _name.find('a')
            _url = 'https://www.pro-football-reference.com' + _a['href']
            self._parse_coach(self.fetch(_url))
            count+=1

            # print(_url)


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
        self.write_csv()


if __name__ == '__main__':
    # try_link = 'https://www.organics.ph/'
    # try_link = 'https://www.vq.org.au/play-learn/find-club/?postcode'

    scraper = Coaches()

    scraper.run()