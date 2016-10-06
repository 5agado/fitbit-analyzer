

def correlateSleepAndSteps(sleepStats, stepsStats, sleepStatName):
    return sleepStats[sleepStatName].corr(stepsStats)