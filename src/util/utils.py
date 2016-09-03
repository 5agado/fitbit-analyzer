import pandas as pd
import json
import os
import sys
import datetime
from datetime import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from util import logger

def loadIntradayData(filepath):
    data = pd.read_csv(filepath, parse_dates=[0], names=['datetime', 'value'])
    return data

def getAllFilepaths(dir):
    SLEEP_FILENAME = 'sleep.csv'

    #Get all paths for sleep files
    subDirs = getAllSubDirsNamesOf(dir)
    filepaths = [os.path.join(folder, SLEEP_FILENAME) for folder in subDirs]
    return filepaths

def loadSleepData(dumpDir):
    SLEEP_VALUE_NONE = 0
    def loadFun(jsonData):
        sleeps = jsonData['sleep']
        if not sleeps:
            return None
        date = datetime.datetime.strptime(sleeps[0]['dateOfSleep'], "%Y-%m-%d").date()
        if len(sleeps)>1:
            logger.info("There are more than one sleep for {}, taking just the first".format(date))
        intradayData = sleeps[0]['minuteData']
        date - datetime.timedelta(days=1)
        dayToSubstract = datetime.timedelta(days=1)
        df = pd.read_json(json.dumps(intradayData), convert_dates=['time'])
        if (df['value']==SLEEP_VALUE_NONE).all():
            logger.info("There are only none values for {}".format(date))
            return None
        df['datetime'] = df.apply(lambda x: datetime.datetime.combine(
           date - dayToSubstract if time(12,00) <= x['dateTime'].time() <=time(23,59) else date,
            x['dateTime'].time()), axis=1)
        df.drop('dateTime', inplace=True, axis=1)
        return df

    return loadData(dumpDir, 'sleep', loadFun)

def loadHBData(dumpDir):
    def loadFun(jsonData):
        intradayData = jsonData['activities-heart-intraday']['dataset']
        date = datetime.datetime.strptime(jsonData['activities-heart'][0]['dateTime'], "%Y-%m-%d").date()
        if not intradayData:
            return None
        df = pd.read_json(json.dumps(intradayData), convert_dates=['time'])
        df['datetime'] = df.apply(lambda x: datetime.datetime.combine(date, x['time'].time()), axis=1)
        df.drop('time', inplace=True, axis=1)
        return df

    return loadData(dumpDir, 'heartbeat', loadFun)

def loadStepsData(dumpDir):
    def loadFun(jsonData):
        intradayData = jsonData['activities-steps-intraday']['dataset']
        date = datetime.datetime.strptime(jsonData['activities-steps'][0]['dateTime'], "%Y-%m-%d").date()
        if not intradayData:
            return None
        df = pd.read_json(json.dumps(intradayData), convert_dates=['time'])
        df['datetime'] = df.apply(lambda x: datetime.datetime.combine(date, x['time'].time()), axis=1)
        df.drop('time', inplace=True, axis=1)
        return df

    return loadData(dumpDir, 'steps', loadFun)

def loadData(dumpDir, dataType, loadFun):
    data = []
    #First level should be the year
    yearDirs = getAllSubDirsNamesOf(dumpDir)
    #Second level should be the date
    for year in yearDirs:
        dates = getAllSubDirsNamesOf(year)
        for date in dates:
            with open("{}\\{}.json".format(date, dataType)) as fileData:
                jsonData = json.load(fileData)
                dayData = loadFun(jsonData)
                if dayData is None:
                    logger.info("No {} measures for {}".format(dataType, date.split('\\')[-1]))
                    continue
                else:
                    data.append(dayData)
    return data

def getAllSubDirsNamesOf(mainDir):
    subDirs = filter(os.path.isdir,
                       [os.path.join(mainDir, subDir) for subDir in os.listdir(mainDir)])
    return subDirs