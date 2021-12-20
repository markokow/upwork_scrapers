import glob
import pandas as pd
from typing import List

extension = 'csv'

data = glob.glob('*.{}'.format(extension))

with open('errors.txt', encoding='utf-8') as f:
    errors = [x.strip() for x in f.readlines()]

def clean_df(df: pd.DataFrame, errors: List):
    data = df.copy()
    for err in errors:
        data = data.applymap(lambda x: x.replace(err,'') if err in str(x) else x)

    return data

for dat in data:
    df = pd.read_csv(dat)
    df = clean_df(df = df, errors=errors)
    df.to_csv(dat)

print("Successfully removed all errors.")







