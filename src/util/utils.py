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

#TODO implement and test loading more than one intraday interval
def loadSleepData(dumpDir):
    """
    Load sleep data from dumping done using the official Fitbit API.
    Check README file for further info
    :param dumpDir: the folder where the date has been dumped
    :return: a list of dataframes, one for each day, containing the intraday sleep data
    """
    SLEEP_VALUE_NONE = 0
    def loadFun(jsonData):
        sleeps = jsonData['sleep']
        if not sleeps:
            return None
        date = datetime.datetime.strptime(sleeps[0]['dateOfSleep'], "%Y-%m-%d").date()
        if len(sleeps)>1:
            logger.info("There are more than one sleep for {}, taking just the first".format(date))
        intradayData = sleeps[0]['minuteData']
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

    return _loadData(dumpDir, 'sleep', loadFun)

def loadHBData(dumpDir):
    """
    Load heart-rate data from dumping done using the official Fitbit API.
    Check README file for further info
    :param dumpDir: the folder where the date has been dumped
    :return: a list of dataframes, one for each day, containing the intraday heart-rate data
    """
    def loadFun(jsonData):
        summaryData = jsonData['activities-heart']
        date = datetime.datetime.strptime(summaryData[0]['dateTime'], "%Y-%m-%d").date()
        if len(summaryData)!=1:
            logger.info("There are {} heart data entries for {}".format(len(summaryData), date))
        intradayData = jsonData['activities-heart-intraday']['dataset']
        if not intradayData:
            return None
        df = pd.read_json(json.dumps(intradayData), convert_dates=['time'])
        df['datetime'] = df.apply(lambda x: datetime.datetime.combine(date, x['time'].time()), axis=1)
        df.drop('time', inplace=True, axis=1)
        return df

    return _loadData(dumpDir, 'heartbeat', loadFun)

# TODO load heartRateZones data
def loadHBSummaryData(dumpDir):
    """
    Load heart-rate summary data from dumping done using the official Fitbit API.
    Check README file for further info
    :param dumpDir: the folder where the date has been dumped
    :return: a list of tuples, one for each day, containing summary heart-rate info
    """
    def loadFun(jsonData):
        summaryData = jsonData['activities-heart']
        date = datetime.datetime.strptime(summaryData[0]['dateTime'], "%Y-%m-%d").date()
        if len(summaryData)!=1:
            logger.info("There are {} heart data entries for {}".format(len(summaryData), date))

        restingHeartRate = summaryData[0]['restingHeartRate']
        return date, restingHeartRate

    return _loadData(dumpDir, 'heartbeat', loadFun)

def loadStepsData(dumpDir):
    """
    Load steps data from dumping done using the official Fitbit API.
    Check README file for further info
    :param dumpDir: the folder where the date has been dumped
    :return: a list of dataframes, one for each day, containing the intraday steps data
    """
    def loadFun(jsonData):
        intradayData = jsonData['activities-steps-intraday']['dataset']
        date = datetime.datetime.strptime(jsonData['activities-steps'][0]['dateTime'], "%Y-%m-%d").date()
        if not intradayData:
            return None
        df = pd.read_json(json.dumps(intradayData), convert_dates=['time'])
        df['datetime'] = df.apply(lambda x: datetime.datetime.combine(date, x['time'].time()), axis=1)
        df.drop('time', inplace=True, axis=1)
        return df

    return _loadData(dumpDir, 'steps', loadFun)

def loadTotalSteps(dumpDir):
    """
    Load total steps count from dumping done using the official Fitbit API.
    Check README file for further info
    :param dumpDir: the folder where the date has been dumped
    :return: a dataframe containing the total steps count indexed by day
    """
    def loadFun(jsonData):
        data = jsonData['activities-steps']
        date = datetime.datetime.strptime(data[0]['dateTime'],
                                          "%Y-%m-%d").date()
        if len(data)!=1:
            logger.info("There are {} steps data entries for {}".format(len(data), date))
        totalSteps = int(data[0]['value'])
        return date, totalSteps

    entries = _loadData(dumpDir, 'steps', loadFun)
    return pd.DataFrame(entries, columns=['datetime', 'value']).set_index(['datetime'])

def _loadData(dumpDir, dataType, loadFun):
    """
    Helper method.
    For the data-dump folder there should be one folder per year, and then one sub-folder for each day,
    in which the different files are generated (e.g. sleep.json, steps.json)
    :param dumpDir: the folder where the date has been dumped
    :param dataType: the type of data to be loaded, equivalent to the name of the corresponding file
    :param loadFun: function defining the procedure for the data loading
    :return: a list of objects had defined in loadFun
    """
    data = []
    # First level should be the year
    yearDirs = getAllSubDirsNamesOf(dumpDir)
    # Second level should be the date
    for year in yearDirs:
        dates = getAllSubDirsNamesOf(year)
        for date in dates:
            # Dumped files are named <dataType>.json
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