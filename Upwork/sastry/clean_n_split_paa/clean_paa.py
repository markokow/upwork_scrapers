import glob
import pandas as pd
from typing import List
import os
import numpy as np

extension = 'csv'
rows_max = 20

data = glob.glob('*.{}'.format(extension))

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
    df.to_csv(os.path.join('Output',f"{dat}_cleaned.csv"), index = False, encoding='utf-8-sig')

print("All csvs sucessfully cleaned. Please check the Output folder")







