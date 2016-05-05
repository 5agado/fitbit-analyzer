import pandas as pd
import numpy as np
from enum import Enum
from datetime import time

from util import utils


class SleepValue(Enum):
    none = 0
    sleeping = 1
    restless = 2
    awake = 3

SLEEP_VALUES = {x.value:x.name for x in SleepValue}

STATS_NAME_BASIC = 'basicStats'
STATS_NAME_TIMING = 'timingStats'
STATS_NAME_BASIC_AND_TIMING = 'basicAndTimingStats'
STATS_NAME_INTERVALS = 'intervalsStats'
STATS_NAME_INTRADAY = 'intradayStats'

def generateStatsFrom(folder, statsType, **kwargs):
    """

    :param folder: folder where the fitbit data dump is.
    Should contain one sub-folder for each day
    :return:
    """
    filepaths = utils.getAllFilepaths(folder)
    filesData = []

    for path in filepaths:
        data = utils.loadIntradayData(path)
        #Filter out empty records (all values equals to zero)
        if (data['value']==SleepValue.none.value).all():
            continue
        filesData.append(data)

    if statsType == STATS_NAME_BASIC:
        stats = generateBasicStats(filesData)
    elif statsType == STATS_NAME_TIMING:
        stats = generateTimingStats(filesData, **kwargs)
    elif statsType == STATS_NAME_BASIC_AND_TIMING:
        basicStats = generateBasicStats(filesData)
        timingStats = generateTimingStats(filesData, **kwargs)
        stats = pd.concat([basicStats, timingStats], axis=1)
    elif statsType == STATS_NAME_INTERVALS:
        stats = generateIntervalsStats(filesData, **kwargs)
    elif statsType == STATS_NAME_INTRADAY:
        stats = generateIntradayStats(filesData, **kwargs)
    else:
        raise Exception(statsType + ' Stat not implemented')
    return stats

#Each row is a day with basic stats like sleep values count, efficiency and total minutes
def generateBasicStats(filesData):
    #Create new df to store the stats
    basicStats = pd.DataFrame(columns=[1,2,3,'total_minutes','sleep_efficiency'])

    #For each file-data, extract the basic stats, and add them to the df
    for fileData in filesData:
        stats = fileData.groupby(['value'], as_index=False).size()
        stats['total_minutes'] = stats.sum()
        date = getSleepDate(fileData)
        basicStats.loc[date] = stats

    #Derive additional stats
    basicStats = basicStats.fillna(0).astype(int)
    basicStats['sleep_efficiency'] = (basicStats[SleepValue.sleeping.value]/basicStats['total_minutes'])*100
    basicStats['sleep_inefficiency'] = (basicStats['sleep_efficiency']-100).abs()
    basicStats['sleep_hours'] = (basicStats[SleepValue.sleeping.value]/60).astype(int) \
                                + (basicStats[SleepValue.sleeping.value]%60)/100
    basicStats['total_hours'] = (basicStats['total_minutes']/60).astype(int) \
                                + (basicStats['total_minutes']%60)/100

    #Rename columns
    columns = SLEEP_VALUES
    columns['value'] = 'date'
    basicStats.rename(columns=columns, inplace=True)
    return basicStats

#Each row is a day with timing stats about like first minute asleep, interval avg and max length
def generateTimingStats(filesData, minSleepIntervalRequired=0):
    #Create new df to store the stats
    intervalsStats = pd.DataFrame(columns=['first_min_asleep',
                                           'to_bed_time',
                                           'wake_up_time',
                                           'sleep_interval_max_len',
                                           'sleep_interval_avg_len'])

    #For each file-data, extract the basic stats, and add them to the df
    for fileData in filesData:
        firstMinuteAsleep = getFirstMinuteAsleep(fileData, minSleepIntervalRequired)
        stats = getSleepIntervalsStats(fileData, minSleepIntervalRequired)
        date = getSleepDate(fileData)
        intervalsStats.loc[date] = [firstMinuteAsleep, fileData.iloc[0]['datetime'].time(),
                                    fileData.iloc[-1]['datetime'].time(),
                                    stats.len.max(), stats.len.mean()]

    return intervalsStats

#Each row is a day with length of all its sleep intervals
def generateIntervalsStats(filesData, minSleepIntervalRequired=0):
    #Create new df to store the stats
    intervalsStats = pd.DataFrame(columns=np.arange(20))

    #For each file-data, extract the basic stats, and add them to the df
    for fileData in filesData:
        stats = getSleepIntervalsStats(fileData, minSleepIntervalRequired)
        date = getSleepDate(fileData)
        intervalsStats.loc[date] = stats.len

    return intervalsStats

#Each row is a complete intraday value array for the corresponding day
def generateIntradayStats(filesData, useTime=True):
    #Create new df to store the stats
    if useTime:
        minutes = pd.date_range('00:00', '23:59', freq='1min')
        intervalsStats = pd.DataFrame(columns=[x.time().strftime("%H:%M")
                                               for x in minutes])
    else:
        intervalsStats = pd.DataFrame(columns=np.arange(600))

    #For each file-data, extract the basic stats, and add them to the df
    for fileData in filesData:
        date = getSleepDate(fileData)
        fileData['time'] = [x.strftime("%H:%M") for x in fileData['datetime'].dt.time]
        fileData.set_index(['time'], inplace=True)
        intervalsStats.loc[date] = fileData['value']

    return intervalsStats

#----------------------------#
#    SECOND LEVEL METHODS    #
#----------------------------#

def getSleepIntervalsStats(data, minSleepIntervalRequired=0):
    sleepIntervals = getSleepIntervals(data, minSleepIntervalRequired)

    #Create new df to store the stats
    stats = pd.DataFrame(columns=['minute_start','minute_end','time_start','time_end','len'])

    #For each interval get start, end, len stats, and add it to the df
    for i, interval in enumerate(sleepIntervals):
        #Substract one because interval indicated the minute, and starts from 1
        timeStart = data.iloc[interval[0]-1]['datetime']
        timeEnd = data.iloc[interval[1]-1]['datetime']
        stats.loc[i] = [interval[0], interval[1], timeStart, timeEnd, interval[1] - interval[0]]

    return stats

#Return the date associated with the provides sleep data.
#It should be the date associated with the first recorded minute, but if this is after
#midnight and before noon, we want to consider the previous day.
def getSleepDate(data):
    firstDatetime = data.ix[0]['datetime']
    if time(12,00) <= firstDatetime.time()<=time(23,59):
        return firstDatetime.date()
    else:
        return (firstDatetime - pd.DateOffset(1)).date()


def getFirstMinuteAsleep(data, minSleepIntervalRequired=0):
    firstAsleep = None

    values = data['value']
    indxs = values[values==SleepValue.sleeping.value].index
    for indx in indxs:
        if (len(values[indx:indx+minSleepIntervalRequired]) >= minSleepIntervalRequired and
                (values[indx:indx+minSleepIntervalRequired]==SleepValue.sleeping.value).all()):
            #Indexing starts from 0, minutes start from 1
            firstAsleep = indx+1
            break

    return firstAsleep

def getSleepIntervals(data, minSleepIntervalRequired=0):
    values = data['value']
    splits = np.append(np.where(np.diff(values)!=0)[0], [len(values)-1])+1

    prev = 0
    intervals = []
    for split in splits:
        if values[prev] == SleepValue.sleeping.value and (split-prev)>=minSleepIntervalRequired:
            intervals.append((prev+1, split))
        prev = split

    return intervals



