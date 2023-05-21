import os
import pandas as pd
import json
import pathlib
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from read_local_data import read_local_data

def plot_selected_data(data, agregate_selection):
    timestamps = np.array(list(data.keys()))
    # Dictionary, key = column name in data, values are dataframes with the agregates as columns, e.g., ['sum', 'mean', ...] 
    agregate_datafields = {columname: pd.DataFrame(columns=agregate_selection) for columname in data[timestamps[0]].columns}

    # Place data into new dataframes for easier plotting
    timeAxis = []
    for timestamp in timestamps:
        values = data[timestamp].loc[agregate_selection]
        for columname in values.columns:      
            agregate_datafields[columname] = pd.concat([agregate_datafields[columname], values.loc[:,columname].to_frame().T], ignore_index=True)
        
        timeAxis.append(datetime.strptime(timestamp, '%Y-%m-%d--%H-%M-%S'))

    number_of_plots = len(agregate_datafields)
    plot_columns = 3

    plot_rows = number_of_plots // plot_columns
    if number_of_plots % plot_columns != 0:
        plot_rows += 1
    
    Position = range(1,number_of_plots + 1)

    fig = plt.figure(1); k=0
    for data_name, df in agregate_datafields.items():
        ax = fig.add_subplot(plot_rows, plot_columns, Position[k])
        k += 1
        
        ax.plot(timestamps, df)
        ax.set_ylabel(data_name)
        ax.legend(agregate_selection)
        ax.set_xticks([timestamps[0], timestamps[-1]])
    
    plt.show()


if __name__ == "__main__":
    script_path = pathlib.Path(__file__).parent.resolve()
    data_path = rf"{script_path}/data"
    
    time_selection = ['2023-05-21--14-28-00', '2023-05-21--19-21-00']
    # Can pass columns to get only wanted columns
    data = read_local_data(data_path, time_selection)

    agregate_selection = ['sum', 'mean', 'max']
    plot_selected_data(data, agregate_selection)