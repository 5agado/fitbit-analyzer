import numpy as np
import pandas as pd

def combineHbAndToggl(togglData, hbData):
    """
    Combine Toggl data and heart-rate data, creating a summary of heart-rate info
    for each Toggl entry (based on date and time correspondence)
    :param togglData: dataframe of toggl data
    :param hbData: heart-rate dataframe
    :return: resulting dataframe of original toggl data + hb stats
    """

    def computeHbStats(togglRow, hbData):
        hb = hbData[(hbData['datetime'] > togglRow['Start'])
                    & (hbData['datetime'] < togglRow['End'])]['value']
        # hb = hb_data.between_time(toggl_row['Start'], toggl_row['End'])
        stats = {'count': hb.count(),
                 'mean': hb.mean(),
                 'min': hb.min(),
                 'max': hb.max(),
                 'std': hb.std()
        }
        return pd.Series(stats)

    # compute hb stats using previous function, and join to toggl data
    combinedStats = togglData.join(togglData.apply(lambda x: computeHbStats(x, hbData), axis=1))

    # remove entries for which no hb stats are present (any apart from count would work)
    combinedStats = combinedStats.dropna(how='all', subset=['max', 'mean', 'min', 'std'])

    return combinedStats

def correlateSleepAndSteps(sleepStats, stepsStats, sleepStatName):
    return sleepStats[sleepStatName].corr(stepsStats)

def tranformToGrowthFromStart(stats):
    res = stats.apply(lambda x: x / x[0])
    return res

def tranformToGrowthFromPrevious(stats):
    res = stats.apply(lambda x: x - x.shift(1))
    return res

def tranformToGrowthFromPreviousLog(stats):
    res = stats.apply(lambda x: np.log(x) - np.log(x.shift(1)))
    return res

def normalize(row):
    return row - row.mean()

def timeToInt(time):
    hour = time.hour
    return (hour * 60) + time.minute

def pivotedTimeToInt(time, pivot, max_val=23):
    hour = time.hour
    if hour >= pivot:
        return ((hour - pivot) * 60) + time.minute
    else:
        return ((max_val - (pivot - hour) ) * 60) + time.minute