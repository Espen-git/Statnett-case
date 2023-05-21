import os
import pandas as pd
import json
import pathlib

def get_date(string):
    return string[0:10].replace('-','')

def get_time(string):
    return string[12:20].replace('-','')


def read_local_data(data_path, time_selection, columns = 
                    ["CO2Emission", "ProductionGe100MW", "ProductionLt100MW", "SolarPower", "OffshoreWindPower",
                    "OnshoreWindPower", "Exchange_Sum", "Exchange_DK1_DE", "Exchange_DK1_NL", "Exchange_DK1_NO", 
                    "Exchange_DK1_SE", "Exchange_DK1_DK2", "Exchange_DK2_DE", "Exchange_DK2_SE", "Exchange_Bornholm_SE"]):
    # read filenames
    start_date = get_date(time_selection[0])
    end_date = get_date(time_selection[1])
    start_time = get_time(time_selection[0])
    end_time = get_time(time_selection[1])

    json_files = [f for f in os.listdir(f"{data_path}/") if ( f.endswith('.json') ) and
                                                            ( get_date(f) >= start_date and get_time(f) >= start_time ) and
                                                            ( get_date(f) <= end_date and get_time(f) <= end_time )]

    # Read data from files and store in dictionary
    jsons_data = {}
    for js in json_files:
        with open(f"{data_path}/{js}", "r") as json_file:
            json_text = json.load(json_file)
            jsons_data.update( {js.replace('.json', ''): pd.DataFrame(json_text).loc[:, columns]} )

    return jsons_data

if __name__ == "__main__":
    script_path = pathlib.Path(__file__).parent.resolve()
    data_path = rf"{script_path}/data"

    time_selection = ['2023-05-21--14-28-00', '2023-05-21--16-30-00']
    data = read_local_data(data_path, time_selection)
    #print(len(data))