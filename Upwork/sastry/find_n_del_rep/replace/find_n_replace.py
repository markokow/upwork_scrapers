import pandas as pd
import pathlib
import os

extension = 'csv'
data = list(pathlib.Path('inputs').glob('*.csv'))

def clean_df(df: pd.DataFrame, _to_replace: pd.DataFrame):
    for idx in _to_replace.index:
        _find = _to_replace.loc[idx, "find"]
        _replace = _to_replace.loc[idx, "replace"]
        _column = _to_replace.loc[idx, "column"]

        if pd.isna(_column):
            df = df.apply(lambda x: x.replace(_find,_replace) if _find in str(x) else x)
        else:
            _col_name = df.columns[int(_column)]
            df[_col_name] = df[_col_name].apply(lambda x: x.replace(_find,_replace) if _find in str(x) else x)

    return df

def run_main(*, _to_replace: pd.DataFrame):
    global data

    for dat in data:
        print(dat)
        df = pd.read_csv(dat, encoding='utf-8')
        df = clean_df(df = df, _to_replace = _to_replace)

        filename = os.path.basename(dat)

        df.to_csv(os.path.join('outputs',filename), index = False, encoding='utf-8-sig')

    print("Successfully replaced all finds.")

output_folder_path = os.path.join(os.getcwd(), 'outputs')

if not(os.path.exists(output_folder_path)):
    os.makedirs(output_folder_path)

try:
    _to_replace = pd.read_csv("to_replace.csv", encoding='utf-8')
    run_main(_to_replace = _to_replace)

except Exception as e:
    print(e)
    print("to_replace.csv does not exist! exiting...")
