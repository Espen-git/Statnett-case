import os
import pandas as pd
import json
import requests
import pathlib
import datetime
import time
import sys
import threading

def read_and_save_data(data_path, agregate_functions=['sum', 'mean', 'max', 'min'], limit='5'):
    response = requests.get(
        url='https://api.energidataservice.dk/dataset/PowerSystemRightNow?limit=' + limit)
    result = response.json()

    records = result.get('records', [])                                    
    records_dataframe = pd.DataFrame(records)

    # Reformat newest UTC timestamp to use as filename
    filename = str(records_dataframe.iloc[0,0])
    filename = filename.replace(":", "-")
    filename = filename.replace("T", "--")
  
    data = records_dataframe.iloc[:, 2:]
    agregate = data.aggregate(agregate_functions, 0)
    # convert to json and save data
    agregate.to_json(rf"{data_path}/{filename}.json")

def run(lock, *args):
    while True:
        try:
            read_and_save_data(*args)
            with lock:
                print(f'Data downloaded at, {datetime.datetime.now()}')
            time.sleep(30)
        except:
            with lock:
                print(f"Something went wrong at, {datetime.datetime.now()}")
            time.sleep(2)
        
if __name__ == "__main__":
    script_path = pathlib.Path(__file__).parent.resolve()
    data_path = rf"{script_path}/data"

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    args = (data_path)
    lock = threading.Lock()
    t = threading.Thread(target=run, args=(lock, args,), daemon=True)
    t.start()

    while True:
        inp = input() 
        if inp.lower() in ('end', 'stop', 'exit'):
            sys.exit('User terminated program')
        else:
            print('Use end, stop or exit to stop program')   
