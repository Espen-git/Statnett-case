import numpy as np
import matplotlib.pyplot as plt

import os
import pandas as pd
import json
import requests
import pathlib
import xarray

script_path = pathlib.Path(__file__).parent.resolve()

limit = '5'
response = requests.get(
    url='https://api.energidataservice.dk/dataset/PowerSystemRightNow?limit=' + limit)
result = response.json()

records = result.get('records', [])                                    

records_dataframe = pd.DataFrame(records)

timestamps = records_dataframe.iloc[:, [0, 1]]

data = records_dataframe.iloc[:, 2:]
agregate = data.aggregate(['sum', 'mean', 'max', 'min'], 0)

filename = str(timestamps.iloc[0,0])
filename = filename.replace(":", "-")
filename = filename.replace("T", "--")

# convert to json and save data
agregate.to_json(rf"{script_path}/data/{filename}.json")


# read filenames
json_files = [pos_json for pos_json in os.listdir(f"{script_path}/data/") if pos_json.endswith('.json')]

# Input from user
columns = ["CO2Emission", "ProductionGe100MW", "ProductionLt100MW", "SolarPower", "OffshoreWindPower",
           "OnshoreWindPower", "Exchange_Sum", "Exchange_DK1_DE", "Exchange_DK1_NL", "Exchange_DK1_NO", 
           "Exchange_DK1_SE", "Exchange_DK1_DK2", "Exchange_DK2_DE", "Exchange_DK2_SE", "Exchange_Bornholm_SE"]

# Read data from files and store in dictionary
jsons_data = {}
for js in json_files:
    with open(f"{script_path}/data/{js}", "r") as json_file:
        json_text = json.load(json_file)
        jsons_data.update( {js: pd.DataFrame(json_text).loc[:, columns]} )


# TODO plot data



# TODO run continusly and repeat every minute
# TODO start/stop input
# TODO ploting interface   