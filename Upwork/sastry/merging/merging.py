import glob
import pandas as pd
from datetime import datetime

extension = 'csv'

data = glob.glob('*.{}'.format(extension))

final_df = pd.DataFrame()

for dat in data:
    df = pd.read_csv(dat)
    cols  = [' ' if ('Unnamed') in str(x) else x for x in df.columns]
    df.columns = cols
    if final_df.empty:
        final_df = df
    else:
        final_df = pd.concat([final_df, df], axis = 0)


numbers = range(0,len(final_df))
final_df[' '] = numbers
now = str(datetime.today()).replace(':','-')
final_df.to_csv(f"{now}.csv", index = False)

print(f"All csvs sucessfully merged to {now}.csv")
