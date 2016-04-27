import pandas as pd
import os

def loadIntradayData(filepath):
    data = pd.read_csv(filepath, parse_dates=[0], names=['datetime', 'value'])
    return data

def getAllFilepaths(folder):
    SLEEP_FILENAME = 'sleep.csv'

    #Get all paths for sleep files
    subFolders = filter(os.path.isdir,
                       [os.path.join(folder, subFolder) for subFolder in os.listdir(folder)])
    filepaths = [os.path.join(folder, SLEEP_FILENAME) for folder in subFolders]
    return filepaths