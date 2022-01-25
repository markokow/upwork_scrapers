import glob
from this import d
import pandas as pd
from typing import List

extension = 'csv'

data = glob.glob('*.{}'.format(extension))

def split_dfs(df: pd.DataFrame, filename: str, columns: List, rows_max: int):
    counter = 0;
    data = pd.DataFrame()

    filename = filename.replace('.csv', '')

    while True:
        if (counter+1)*rows_max > len(df):
            data = df.iloc[counter*rows_max:,:]
            data.to_csv(f"{filename}_part_{counter+1}.csv", index = False, encoding='utf-8')
            break
        else:
            data = df.iloc[counter*rows_max:(counter+1)*rows_max,:]
            data.to_csv(f"{filename}_part_{counter+1}.csv", index = False, encoding='utf-8')
        counter += 1

for dat in data:
    try:
        df = pd.read_csv(dat, encoding = 'utf-8')
    except:
        df = pd.read_csv(dat, encoding = 'unicode_escape')
    cols  = ['' if ('Unnamed') in str(x) else x for x in df.columns]
    df.columns = cols
    df = split_dfs(df = df, filename = dat, columns = cols, rows_max=150)

print("All csvs sucessfully splitted.")







