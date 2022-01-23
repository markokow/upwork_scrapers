import glob
from this import d
import pandas as pd
from typing import List

extension = 'csv'

data = glob.glob('*.{}'.format(extension))

def concatenate_dfs(df: pd.DataFrame, filename: str):

    data = pd.DataFrame()
    rows = len(df)

    df = df.astype(str)
    for col in df.columns:
        if col == '':
            data[''] = df[col]
            continue
        elif 'question' in col.lower():
            if 'concatenated' not in data:
                data['concatenated'] = '<h2>' + df[col] + '</h2>'
            else:
                for i in range(0, rows):
                    if df.loc[i, col] == '':
                        continue
                    else:
                        data.loc[i,'concatenated'] = data.loc[i, 'concatenated'] + '\n' + '<h2>' + df.loc[i,col] + '</h2>'
        else:
            for i in range(0, rows):
                if df.loc[i, col] == '':
                    continue
                else:
                        data.loc[i,'concatenated'] = data.loc[i,'concatenated'] + '\n' + df.loc[i,col] 

    data.index = df.index
    data.to_csv(filename, index = False)

for dat in data:
    df = pd.read_csv(dat)
    cols  = ['' if ('Unnamed') in str(x) else x for x in df.columns]
    df.columns = cols
    df = concatenate_dfs(df = df, filename = dat)

print("All csvs sucessfully concatenated.")







