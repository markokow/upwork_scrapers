import glob
import pandas as pd
from typing import List
import os
import numpy as np

extension = 'csv'
rows_max = 20

data = glob.glob('*.{}'.format(extension))

def split_dfs(*, df: pd.DataFrame, filename: str, columns: List, rows_max: int):
    counter = 0
    data = pd.DataFrame()

    filename = filename.replace('.csv', '')

    while True:
        if (counter+1)*rows_max > len(df):
            data = df.iloc[counter*rows_max:,:]
            data.to_csv(os.path.join('Output',f"{filename}_part_{counter+1}.csv"), index = False, encoding='utf-8-sig')
            break
        else:
            data = df.iloc[counter*rows_max:(counter+1)*rows_max,:]
            data.to_csv(os.path.join('Output',f"{filename}_part_{counter+1}.csv"), index = False, encoding='utf-8-sig')
        counter += 1

output_folder_path = os.path.join(os.getcwd(), 'Output')

if not(os.path.exists(output_folder_path)):
    os.makedirs(output_folder_path)

for dat in data:
    print(dat)
    df = pd.DataFrame()
    try:
        df = pd.read_csv(dat, encoding = 'utf-8')
    except:
        df = pd.read_csv(dat, encoding = 'unicode_escape')
    
    cols  = ['' if ('Unnamed') in str(x) else x for x in df.columns]
    df = df.dropna(subset=['question_1'])
    
    df[df.columns[0]] = np.arange(len(df)) + 1

    df.columns = cols
    df = split_dfs(df = df, filename = dat, columns = cols, rows_max=rows_max)

print("All csvs sucessfully splitted.")







