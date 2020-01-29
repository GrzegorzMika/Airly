import pandas as pd
import os

path = '/home/airly/data'
files = os.listdir(path)

if os.path.exists(os.path.join(path, 'merged.txt')):
    merged = pd.read_csv(os.path.join(path, 'merged.txt'), sep='\n', header=None)
    merged = pd.Series(merged.iloc[:,0]).tolist()
else:
    merged = []

files = [file for file in files if file not in [merged, 'airly_data.csv', 'merged.txt', 'log.log']]

data =[pd.read_csv(os.path.join(path, file)) for file in files]
data = pd.concat(data)

if os.path.exists(os.path.join(path, 'airly_data.csv')):
    airly_data = pd.read_csv(os.path.join(path, 'airly_data.csv'))
    airly_data = pd.concat([airly_data, data])
    airly_data.to_csv(os.path.join(path, 'airly_data.csv'))
    merged = pd.DataFrame(merged + files)
    merged.to_csv(os.path.join(path, 'merged.txt'), sep='\n', header=False, index=False)
else:
    data.to_csv(os.path.join(path, 'airly_data.csv'))
    pd.DataFrame(files).to_csv(os.path.join(path, 'merged.txt'), sep='\n', header=False, index=False)