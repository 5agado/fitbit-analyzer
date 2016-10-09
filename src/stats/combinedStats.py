import numpy as np

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
    return (time.hour*60) + time.minute