"""Example of Implementing a ML forecasting model for Steamboat

This script demonstrates how to create and test a machine learning 
forecasting model using seismic data from steamboat geayser.

Author: Alberto Ardid
Email: aardids@gmail.com
Version: 0.1.0
"""

from datetime import timedelta
# from puia.tests import run_tests  # Uncomment if running tests
from puia.model import ForecastModel, MultiVolcanoForecastModel, MultiDataForecastModel
from puia.data import SeismicData, GeneralData
from puia.utilities import datetimeify, load_dataframe
from glob import glob
from sys import platform
import pandas as pd
import numpy as np
import os, shutil, json, pickle, csv
import matplotlib.pyplot as plt

# Define time constants for easier date handling
_MONTH = timedelta(days=365.05 / 12)
_DAY = timedelta(days=1)

def forecast_test():
    """
    Test the forecast model by training on Whakaari and forecasting on Bezymianny.

    This function initializes the data streams, sets up the MultiVolcanoForecastModel,
    trains the model, and performs high-resolution forecasting for a specific eruption event.
    """
    # Define data ranges for each volcano
    data = {
        'YNM': ['2018-01-04','2018-12-31'],  # Steamboat data range
    }

    # Define eruption indices for each volcano
    eruptions = {
        'YNM': [i for i in range(0, 32)],  # Placeholder for eruption events at YNM
    }

    # Define seismic data streams to use in the model
    # 'zsc2_' indicates standardization; 'F' indicates outlier filtering (e.g., regional earthquakes)
    data_streams = ['rsam']#['zsc2_rsamF', 'zsc2_mfF', 'zsc2_hfF', 'zsc2_dsarF']

python
Copy code
# 'zsc2_' indicates standardization; 'F' indicates outlier filtering (e.g., regional earthquakes)
data_streams = ['zsc2_rsamF',]  # Additional streams: 'zsc2_mfF', 'zsc2_hfF', 'zsc2_dsarF'

    # Create a MultiVolcanoForecastModel instance
    fm = MultiVolcanoForecastModel(
        data=data,               # Volcano data ranges
        window=1.0,              # Forecasting window (days)
        overlap=0.75,            # Overlap fraction between windows
        look_forward=1.0,        # Look-forward period (days)
        data_streams=data_streams,  # Seismic data streams
        root='test'              # Directory for saving results
    )

    # Define features to drop during training
    drop_features = ['linear_trend_timewise', 'agg_linear_trend']

    # Load eruption times for YNM from a file
    fl_nm = 'data' + os.sep + 'YNM' + '_eruptive_periods.txt'
    with open(fl_nm, 'r') as fp:
        tes = [datetimeify(ln.rstrip()) for ln in fp.readlines()]

    # Define eruption period of interest for YNM
    te = tes[23]  # Use the first eruption event
    tf = te + _DAY * 2  # End time: 2.5 days after eruption
    ti = te - _DAY * 4  # Start time: 12.5 days before eruption

    # Exclude data around eruptions to avoid overfitting
    exclude_dates = {}
    for _sta in data.keys():  # Initialize exclusions for all stations
        exclude_dates[_sta] = None
    exclude_dates['YNM'] = [[ti, tf]]  # Exclude data for YNM during the eruption period

    # Train the model
    fm.train(
        drop_features=drop_features,  # Features to exclude
        retrain=True,                # Avoid retraining if already trained
        Ncl=200,                      # Number of clusters for feature extraction
        n_jobs=4,                     # Parallel processing jobs
        exclude_dates=exclude_dates   # Dates to exclude for training
    )

    # Perform high-resolution forecasting for YNM
    fm.hires_forecast(
        station='YNM',          # Station to forecast
        ti=ti,                   # Forecast start time
        tf=tf,                   # Forecast end time
        recalculate=True,       # Use cached results if available
        n_jobs=4,                # Parallel processing jobs
        threshold=0.6,           # Threshold for eruption probabilities
        root='test',             # Root directory for saving results
        save='plots' + os.sep + 'test' + os.sep + '_fc_eruption_' + 'YNM' + '_' + str(eruptions['YNM'][-1]) + '.png'
                                # Path to save the forecast plot
    )


def main():
    """
    Main function to run the forecast test.
    """
    forecast_test()  # Run the forecast test
    pass  # Placeholder for additional functionality


if __name__ == '__main__':
    main()  # Execute the script

