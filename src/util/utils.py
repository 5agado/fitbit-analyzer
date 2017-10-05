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
    Check README file for further info on the scraping process and saved format
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
            logger.info("There are {} sleep records for {}, taking main sleep".format(len(sleeps), date))
        intradayData = None
        for sleep in sleeps:
            if sleep['isMainSleep']:
                intradayData = sleep['minuteData']
                break
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

def loadHBData(dumpDir, concat=False):
    """
    Load heart-rate data from dumping done using the official Fitbit API.
    Check README file for further info on the scraping process and saved format
    :param concat: specify when to concat all entries in a single dataframe
    :param dumpDir: the folder where the date has been dumped
    :return: a list of dataframes, one for each day, containing the intraday heart-rate data.
            or a single one, if concat is set to True.
    """
    def loadFun(jsonData):
        summaryData = jsonData['activities-heart']
        date = summaryData[0]['dateTime']
        if len(summaryData)!=1:
            logger.info("There are {} heart data entries for {}".format(len(summaryData), date))
        intradayData = jsonData['activities-heart-intraday']['dataset']
        if not intradayData:
            return None
        df = pd.read_json(json.dumps(intradayData))
        df['datetime'] = pd.to_datetime(date + ' ' + df['time'])
        df.drop('time', inplace=True, axis=1)
        return df

    if concat:
        return pd.concat(_loadData(dumpDir, 'heartbeat', loadFun), ignore_index=True)
    else:
        return _loadData(dumpDir, 'heartbeat', loadFun)

# TODO load heartRateZones data
def loadHBSummaryData(dumpDir):
    """
    Load heart-rate summary data from dumping done using the official Fitbit API.
    Check README file for further info on the scraping process and saved format
    :param dumpDir: the folder where the date has been dumped
    :return: a list of tuples, one for each day, containing summary heart-rate info
    """
    def loadFun(jsonData):
        summaryData = jsonData['activities-heart']
        date = datetime.datetime.strptime(summaryData[0]['dateTime'], "%Y-%m-%d").date()
        if len(summaryData)!=1:
            logger.info("There are {} heart data entries for {}".format(len(summaryData), date))

        try:
            restingHeartRate = summaryData[0]['value']['restingHeartRate']
        except KeyError:
            logger.info("No resting heart rate info for {}".format(date))
            return None
        return date, restingHeartRate

    entries = _loadData(dumpDir, 'heartbeat', loadFun)
    return pd.DataFrame(entries, columns=['date', 'rhr']).set_index(['date'])

def loadStepsData(dumpDir):
    """
    Load steps data from dumping done using the official Fitbit API.
    Check README file for further info on the scraping process and saved format
    :param dumpDir: the folder where the date has been dumped
    :return: a list of dataframes, one for each day, containing the intraday steps data
    """
    def loadFun(jsonData):
        intradayData = jsonData['activities-steps-intraday']['dataset']
        date = jsonData['activities-steps'][0]['dateTime']
        if not intradayData:
            return None
        df = pd.read_json(json.dumps(intradayData))
        df['datetime'] = pd.to_datetime(date + ' ' + df['time'])
        df.drop('time', inplace=True, axis=1)
        return df

    return _loadData(dumpDir, 'steps', loadFun)

def loadTotalSteps(dumpDir):
    """
    Load total steps count from dumping done using the official Fitbit API.
    Check README file for further info on the scraping process and saved format
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
    return pd.DataFrame(entries, columns=['date', 'steps']).set_index(['date'])

#TODO maybe better to return a dictionary? Or for some types it will not work
def _loadData(dumpDir, dataType, loadFun):
    """
    Helper method.
    For the data-dump folder there should be one folder per year, and then one sub-folder for each day,
    in which the different files are generated (e.g. sleep.json, steps.json)
    :param dumpDir: the folder where the date has been dumped
    :param dataType: the type of data to be loaded, equivalent to the name of the corresponding file
    :param loadFun: function defining the procedure for the data loading
    :return: a list of objects as defined in loadFun
    """
    data = []
    # First level should be the year
    yearDirs = getAllSubDirsNamesOf(dumpDir)
    # Second level should be the date
    for year in yearDirs:
        dates = getAllSubDirsNamesOf(year)
        for date in dates:
            # Dumped files are named <dataType>.json
            filename = os.path.join(date, dataType) + '.json'
            try:
                with open(filename) as fileData:
                    jsonData = json.load(fileData)
                    dayData = loadFun(jsonData)
                    if dayData is None:
                        logger.info("No {} measures for {}".format(dataType, date.split('\\')[-1]))
                        continue
                    else:
                        data.append(dayData)
            except FileNotFoundError:
                logger.warning("{} not found. Might be cause last scraped day.".format(filename))

    return data

def loadTogglData(reportsPaths, columnsToDrop=None):
    """
    Load a list of toggl reports in a dataframe
    :param reportsPaths: list of reports paths
    :param columnsToDrop: list of names of columns to drop, all need to be present
    :return: all reports unified in a single dataframe
    """
    reports = []
    # for each path, load and add report to list
    for path in reportsPaths:
        # lovely automatic parsing of dates as well as combination of date and time
        report = pd.read_csv(path, parse_dates=[['Start date', 'Start time'],
                                                ['End date', 'End time']])
        # rename datetime columns
        report = report.rename(index=str, columns={"Start date_Start time": "Start",
                                                           "End date_End time": "End"})
        # drop unnecessary fields
        if columnsToDrop:
            report.drop(columnsToDrop, axis=1, inplace=True)
        reports.append(report)
    # concatenate reports in single dataframe
    return pd.concat(reports, ignore_index=True)

def getAllSubDirsNamesOf(mainDir):
    subDirs = filter(os.path.isdir,
                       [os.path.join(mainDir, subDir) for subDir in os.listdir(mainDir)])
    return subDirs