import csv
import requests
import io

from typing import List
from bs4 import BeautifulSoup


class WebA():
    
    def __init__(self):
        self.base_url = 'https://www.mouser.com/Semiconductors/Integrated-Circuits-ICs/Driver-ICs/_/N-7zhz5Z1yzvvqx'

        self.result: List[dict] = []



    def _fetch_site(self, url):

        print("here2")
        response = requests.get(url)

        return response

    def _parse_data(self, response):


        print("here")
        try:
            _content = BeautifulSoup(response.content, 'lxml')
        except:
            raise Exception

        # _data = _content.find('table', id_ = 'SearchResultsGrid_grid').text

        print("SUCESS")
        # 
        #   print(_data.prettify())

        # for data in _content:

            
            # data_dict = {}
            
            # try:
            #     data_dict['Mrf. Part #'] = data.find_element_by_class_name('part-number-lbl')[0].text.strip()
            # except:
            #     data_dict['Mrf. Part #'] = ''

            # try:
            #     data_dict['Mouser Part #'] = data.find_element_by_class_name('part-number-lbl')[-1].text.strip()
            # except:
            #     data_dict['Mouser Part #'] = ''

            # try:
            #     data_dict['Mfr.'] = ' '.join(data.find_element_by_class_name('dr-website').text.strip().split(' ')[1:])
            # except:
            #     data_dict['Mfr.'] = ''

            # try:
            #     data_dict['Description'] = ' '.join(data.find_element_by_class_name('dr-address').text.strip().split(' ')[1:])
            # except:
            #     data_dict['Description'] = ''

            # try:
            #     data_dict['Quantity'] = ' '.join(data.find_element_by_class_name('dr-phone').text.strip().split(' ')[1:])

            # except:
            #     data_dict['Quantity'] = ''

            # try:
            #     data_dict['Status'] = ' '.join(data.find_element_by_class_name('dr-phone').text.strip().split(' ')[1:])

            # except:
            #     data_dict['Status'] = ''

            # if not data_dict['Business Name'] in self.processed_facility:
            # self.result.append(data_dict)
            #     self.processed_facility.add(data_dict['Business Name'])
            # else:
            #     continue

        # self.driver.execute_script("window.history.go(-1)")
    def _run(self,):

        max_count = 1

        for i in range(0,max_count):

            url = self.base_url+f'?No={25*(i)}'
            print('searching url:',url)

            try:
                response = self._fetch_site(self.base_url)

                self._parse_data(response)
            except Exception as e:
                print(e)

        # print(self.result)


    def write_csv(self,):
        '''Save results to csv.'''
        print('Saving to csv....')

        if self.result: 
            with open('results.csv', 'w', newline = '', encoding = 'utf-8') as csv_file:
                writer_object = csv.DictWriter(csv_file, fieldnames = self.result[0].keys())
                writer_object.writeheader()

                for row in self.result:
                    writer_object.writerow(row)
            print("Saved to results.xlsx")
        
        else:
            print('No data was saved')

if __name__ == '__main__':

    scrape = WebA()
    scrape._run()

    # scrape._run()