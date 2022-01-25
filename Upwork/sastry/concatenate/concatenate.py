import glob
from this import d
import pandas as pd
from typing import List

extension = 'csv'

data = glob.glob('*.{}'.format(extension))

errors = ["\"", "'"]

def clean_df(df: pd.DataFrame, errors: List):
    data = df.copy()
    data = data.applymap(lambda x: str(x))
    for err in errors:
        data = data.applymap(lambda x: x.replace(err,'') if err in str(x) else x)

    data = data.applymap(lambda x: x.strip())

    return data

def concatenate_dfs(df: pd.DataFrame, filename: str):

    data = pd.DataFrame()
    rows = len(df)

    df = df.astype(str)
    counter = 0
    for col in df.columns:
        counter += 1
        if counter == 2:
            data['question_1'] = df[col]
            continue
        if col == '' or col == ' ':
            data[''] = df[col]
            continue
        elif 'question' in col.lower():
            if 'concatenated' not in data:
                data['concatenated'] = '<h2>' + df[col] + '</h2>'
            else:
                for i in range(0, rows):
                    if df.loc[i, col] == '' or df.loc[i, col] == ' ':
                        continue
                    else:
                        data.loc[i,'concatenated'] = data.loc[i, 'concatenated'] + '\n' + '<h2>' + df.loc[i,col] + '</h2>'
        else:
            if 'concatenated' not in data:
                data['concatenated'] = df[col]
            else:
                for i in range(0, rows):
                    if df.loc[i, col] == '' or df.loc[i, col] == ' ':
                        continue
                    else:
                        data.loc[i,'concatenated'] = data.loc[i,'concatenated'] + '\n' + df.loc[i,col] 
        

    data.index = df.index
    filename = filename.replace('.csv', '')
    data.to_csv(f"{filename}_concatenated.csv", index = False)
    # data.to_csv('results.csv', index = False)

for dat in data:
    df = pd.read_csv(dat)
    cols  = ['' if ('Unnamed') in str(x) else x for x in df.columns]
    df.columns = cols
    errors = ["\"", "'"]
    df = clean_df(df = df, errors=errors)
    df = concatenate_dfs(df = df, filename = dat)

print("All csvs sucessfully concatenated.")







