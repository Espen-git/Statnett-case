import os
import pandas as pd
import json
import pathlib

def read_local_data(data_path):



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

if __name__ == "__main__":
    script_path = pathlib.Path(__file__).parent.resolve()
    data_path = rf"{script_path}/data"