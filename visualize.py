import os
import pandas as pd
import json
import pathlib
import matplotlib.pyplot as plt
import numpy as np
from read_local_data import read_local_data

def plot_selected_data(data, agregate_selection):
    timestamps = np.array(list(data.keys()))
    # Dictionary, key = column name in data, values are dataframes with the agregates as columns, e.g., ['sum', 'mean', ...] 
    agregate_datafields = {columname: pd.DataFrame(columns=agregate_selection) for columname in data[timestamps[0]].columns}

    # Place data into new dataframes for easier plotting
    for timestamp in timestamps:
        values = data[timestamp].loc[agregate_selection]
        for columname in values.columns:      
            agregate_datafields[columname] = pd.concat([agregate_datafields[columname], values.loc[:,columname].to_frame().T], ignore_index=True)

    for data_name, df in agregate_datafields.items():
        df.plot()
        plt.show()


if __name__ == "__main__":
    script_path = pathlib.Path(__file__).parent.resolve()
    data_path = rf"{script_path}/data"
    
    time_selection = ['2023-05-21--14-28-00', '2023-05-21--18-00-00']
    # Can pass columns to get only wanted columns
    data = read_local_data(data_path, time_selection)

    agregate_selection = ['sum', 'mean', 'max']
    plot_selected_data(data, agregate_selection)