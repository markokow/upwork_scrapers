import glob
from xmlrpc.client import boolean
import pandas as pd
from typing import List

extension = 'csv'

data = glob.glob('*.{}'.format(extension))

errors = ["\"", "'"]

def clean_df(df: pd.DataFrame, errors: List):
    data = df.copy()
    data = data.applymap(lambda x: str(x))  
    data = data.applymap(lambda x: x.strip())  
    # data = data.applymap(lambda x: 'no data' if (x == '' or x == ' ') else x)  
    for err in errors:
        data = data.applymap(lambda x: x.replace(err,'') if err in str(x) else x)


    _total: int = 0
    _boolean: bool = False
    _total_true: int = 0

    for i in range(0, len(data)):
        _boolean = False
        for col in data.columns:
            if data.loc[i,col] == '' or data.loc[i,col] == '':
                _boolean = True
                break
        if _boolean == True:
            # print(data.loc[i,' '])
            _total += 1
        else:
            print(data.loc[i, ' '])
            _total_true += 1


    print("total is: ", _total_true)
    data = data.applymap(lambda x: x.strip())

    return data

for dat in data:
    df = pd.read_csv(dat, encoding = 'utf-8')
    # df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.columns = [' ' if ('Unnamed') in str(x) else x for x in df.columns]
    print(df)

    df = df.fillna('')
    df = clean_df(df = df, errors=errors)

    dat = dat.replace('.csv', '')
    df.to_csv(f"{dat}_cleaned.csv", index = False, encoding = 'utf-8')
    # df.to_csv(dat, index = False, encoding = 'utf-8')

print("Files are all ready for wordpress. Filenames are still the same.")