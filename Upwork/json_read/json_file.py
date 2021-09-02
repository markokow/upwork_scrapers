from csv import excel_tab
import json
import os
import glob
import csv
from typing import List

class _json_reader():

    def __init__(self,JSON_CONFIG_FILE_PATH):

        self._paths:List[str] = []
        for file in glob.glob('*.json'):
            self._paths.append(JSON_CONFIG_FILE_PATH + '/' + file)

        #results
        self._data: dict = {}

        #storing reulst
        self._dat_dict: dict = {}
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

    def _read_json(self,_path):

        try:
            with open(_path) as _file:
                self._data = json.load(_file)
        except IOError as e:
            print(e)

    def _parse_dict(self, _data: dict = {}, _key: str = ''):

        for _dat in _data.items():
            if(type(_dat[-1]) == dict):
                self._parse_dict(_dat[-1], _key + ('' if _key == '' else '.') + _dat[0])
            else:
                self._dat_dict [_key + ('' if _key == None else '.') +  _dat[0]] = _dat[-1]



    def _run(self,):

        for _path in self._paths:
            # print(_path)
            self._read_json(_path)

            #restart _dat_dict
            self._dat_dict = {}

            self._parse_dict(self._data)

            value = {k: v for k,v in self._dat_dict.items() if v}
            self._result.append(value)

        self.write_csv()



if __name__ == '__main__':

    #CWD = 
    _cwd = os.getcwd()
    _path = _cwd + '/actual'
    # print(_cwd)
    os.chdir(_path)

    read = _json_reader( JSON_CONFIG_FILE_PATH =_path)
    read._run()