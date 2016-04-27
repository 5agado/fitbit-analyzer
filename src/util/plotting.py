import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plotPreliminaryStats(stats):
    columns = ['sleep_inefficiency', 'restless', 'sleep_interval_avg_len', 'total_hours']
    stats = stats[columns]
    stats.hist()
    sns.plt.show()

def plotWeekdayStats(stats):
    MEASURE_NAME = 'weekday'
    dayOfWeek={0:'Mon', 1:'Tue', 2:'Wed', 3:'Thur', 4:'Fri', 5:'Sat', 6:'Sun'}
    order = ['Mon','Tue','Wed','Thur','Fri','Sat','Sun']
    columns = ['sleep_inefficiency', 'restless', 'sleep_interval_avg_len', 'total_hours',
               'awake', 'first_min_asleep']
    stats[MEASURE_NAME] = stats.date.dt.dayofweek.map(dayOfWeek)

    f, axes = getAxes(2,3)
    for i, c in enumerate(columns):
        sns.boxplot(x=MEASURE_NAME, y=c, data=stats, order=order, ax=axes[i])
    sns.plt.show()
    #plot(stats, columns, MEASURE_NAME, 2, 3, order=order)

def plotMonthlyStats(stats):
    MEASURE_NAME = 'month'
    months={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug',
            9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    columns = ['sleep_inefficiency', 'restless', 'sleep_interval_avg_len', 'total_hours']
    stats[MEASURE_NAME] = stats.date.dt.month.map(months)
    order = [m for m in order if m in stats[MEASURE_NAME].unique()]

    f, axes = getAxes(2,3)
    for i, c in enumerate(columns):
        sns.boxplot(x=MEASURE_NAME, y=c, data=stats, order=order, ax=axes[i])
    sns.plt.show()
    #plot(stats, columns, MEASURE_NAME, 4, 1, order=order)

def plotDailyStats(stats):
    MEASURE_NAME = 'date'
    columns = ['sleep_inefficiency', 'restless', 'total_hours']

    dates = pd.date_range(start=stats.date.iloc[0].date(), end=stats.date.iloc[-1].date())
    stats.set_index(['date'], inplace=True)
    stats = stats.reindex(dates)
    stats.reset_index(inplace=True)
    stats.rename(columns={'index':'date'}, inplace=True)

    #measure = 'sleeping'
    #values = stats[measure]-stats[measure].mean()

    f, axes = getAxes(3,1)
    xTicksDiv = 10
    xticks = [x.date() for x in stats.date]
    keptticks = xticks[::int(len(xticks)/xTicksDiv)]
    xticks = ['' for _ in xticks]
    xticks[::int(len(xticks)/xTicksDiv)] = keptticks
    for i, c in enumerate(columns):
        g =sns.barplot(x=MEASURE_NAME, y=c, data=stats, ax=axes[i])
        g.set_xticklabels([])
    g.set_xticklabels(xticks, rotation=45)
    sns.plt.show()
    #plot(stats, columns, MEASURE_NAME, 4, 1)

def plotSleepValueHeatmap(intradayStats, sleepValue=1):
    data = intradayStats.apply(pd.value_counts)

    xTicksDiv = 10
    xticks = data.columns.values
    keptticks = xticks[::int(len(xticks)/xTicksDiv)]
    xticks = ['' for _ in xticks]
    xticks[::int(len(xticks)/xTicksDiv)] = keptticks
    g = sns.heatmap(data.loc[sleepValue].reshape(1,-1))
    g.set_xticklabels(xticks)
    sns.plt.show()

def getAxes(nrows, ncols):
    f, axes = plt.subplots(nrows=nrows, ncols=ncols)
    axes = axes.reshape(-1)
    return f, axes

def plot(data, columns, measureName, nrows, ncols, order=None):
    f, axes = plt.subplots(nrows=nrows, ncols=ncols)
    axes = axes.reshape(-1)
    for i, c in enumerate(columns):
        sns.boxplot(x=measureName, y=c, data=data, order=order, ax=axes[i])
    sns.plt.show()