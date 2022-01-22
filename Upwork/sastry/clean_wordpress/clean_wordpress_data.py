import glob
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

for dat in data:
    df = pd.read_csv(dat)
    # df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.columns = ['index' if ('Unnamed') in str(x) else x for x in df.columns]
    print(df)

    df = df.fillna('')
    df = clean_df(df = df, errors=errors)
    df.to_csv(dat, index = False)

print("Files are all ready for wordpress. Filenames are still the same.")







