from matplotlib.style import context
import pandas as pd
import pathlib
import os
from typing import List

# extension = 'txt'
data = list(pathlib.Path('inputs').glob('*.txt'))

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

def run_main():
    global data

    final_list: List = []
    for dat in data:
        file = open(dat, "r")
        content = [_.strip() for _ in file.read().split(",")]
        
        final_list = final_list + content

    txtfile = open("final_list.txt", "w")
    for elem in final_list:
        txtfile.write(elem + "\n")
    
    txtfile.close()

    print("Succesfully merged all text files.")

# output_folder_path = os.path.join(os.getcwd(), 'outputs')

# if not(os.path.exists(output_folder_path)):
#     os.makedirs(output_folder_path)

run_main()
