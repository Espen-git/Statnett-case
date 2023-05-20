import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import requests

limit = '5'
response = requests.get(
    url='https://api.energidataservice.dk/dataset/PowerSystemRightNow?limit=' + limit)

result = response.json()

# Prints all data
""" for k, v in result.items(): 
    print(k, v) """

records = result.get('records', [])
                                           
# Prints only the tabular data (records)
""" print('records:') #
for record in records:
    print(' ', record) """

records_dataframe = pd.DataFrame(records)

timestamps = records_dataframe.iloc[:, [0, 1]]

data = records_dataframe.iloc[:, 2:]
agregate = data.aggregate(['sum', 'mean', 'max', 'min'], 0)


print(timestamps)
print(agregate)

# TODO convert to json and save data
# TODO read data
# TODO plot data
# TODO run continusly and repeat every minute
# TODO start/stop input
# TODO ploting interface   