import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats as scipystats

from stats import sleepStats

NAMES={'sleep_inefficiency':'Sleep Inefficiency (%)',
           'restless':'Restless (minutes)',
           'awake':'Awake (minutes)',
           'total_minutes':'Total Minutes',
           'sleep_hours':'Hours of Sleep',
           'first_min_asleep':'First Minute Asleep'}

def plotPreliminaryStats(stats):
    """
    Plot measures distribution using histograms
    :param stats: data to plot
    """
    columns = ['sleep_inefficiency', 'restless', 'awake', 'total_minutes', 'sleep_hours',
               'first_min_asleep']
    stats = stats[columns]
    stats.rename(columns=NAMES, inplace=True)
    #stats['to_bed_hour'] = stats['to_bed_time'].dt.hour
    stats.hist()
    sns.plt.show()

def plotWeekdayStats(stats):
    """
    Plot aggregated (mean) stats by dayOfWeek
    :param stats: data to plot
    """
    MEASURE_NAME = 'weekday'
    dayOfWeek={0:'Mon', 1:'Tue', 2:'Wed', 3:'Thur', 4:'Fri', 5:'Sat', 6:'Sun'}
    order = ['Mon','Tue','Wed','Thur','Fri','Sat','Sun']
    columns = ['sleep_inefficiency', 'restless', 'awake', 'total_minutes', 'sleep_hours',
               'first_min_asleep']
    stats.rename(columns=NAMES, inplace=True)
    stats[MEASURE_NAME] = stats.date.dt.dayofweek.map(dayOfWeek)

    f, axes = getAxes(2,3)
    for i, c in enumerate(columns):
        g = sns.boxplot(x=MEASURE_NAME, y=NAMES[c], data=stats, order=order, ax=axes[i])
        g.set_xlabel('')
    sns.plt.show()
    #plot(stats, columns, MEASURE_NAME, 2, 3, order=order)

def plotMonthlyStats(stats):
    """
    Plot aggregated (mean) stats by month
    :param stats: data to plot
    """
    MEASURE_NAME = 'month'
    months={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug',
            9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    columns = ['sleep_inefficiency', 'restless', 'sleep_hours',
               'first_min_asleep']
    stats.rename(columns=NAMES, inplace=True)
    stats[MEASURE_NAME] = stats.date.dt.month.map(months)
    order = [m for m in order if m in stats[MEASURE_NAME].unique()]

    f, axes = getAxes(2,2)
    for i, c in enumerate(columns):
        g = sns.boxplot(x=MEASURE_NAME, y=NAMES[c], data=stats, order=order, ax=axes[i])
        g.set_xlabel('')
    sns.plt.show()
    #plot(stats, columns, MEASURE_NAME, 4, 1, order=order)

def plotDailyStats(stats):
    """
    Plot daily stats. Fill all data range, and put NaN for days without measures
    :param stats: data to plot
    """
    MEASURE_NAME = 'date'
    columns = ['sleep_inefficiency', 'sleep_hours']
    stats.rename(columns=NAMES, inplace=True)

    dates = pd.date_range(start=stats.date.iloc[0].date(), end=stats.date.iloc[-1].date())
    stats.set_index(['date'], inplace=True)
    stats = stats.reindex(dates)
    stats.reset_index(inplace=True)
    stats.rename(columns={'index':'date'}, inplace=True)

    #measure = 'sleeping'
    #values = stats[measure]-stats[measure].mean()

    f, axes = getAxes(2,1)
    xTicksDiv = 10
    #xticks = [(x-pd.DateOffset(years=1, day=2)).date() for x in stats.date]
    xticks = [x.date() for x in stats.date]
    keptticks = xticks[::int(len(xticks)/xTicksDiv)]
    xticks = ['' for _ in xticks]
    xticks[::int(len(xticks)/xTicksDiv)] = keptticks
    for i, c in enumerate(columns):
        g =sns.barplot(x=MEASURE_NAME, y=NAMES[c], data=stats, ax=axes[i])
        g.set_xticklabels([])
        g.set_xlabel('')
    g.set_xticklabels(xticks, rotation=45)
    sns.plt.show()
    #plot(stats, columns, MEASURE_NAME, 4, 1)

def plotSleepValueHeatmap(intradayStats, sleepValue=1):
    data = intradayStats.apply(pd.value_counts)

    xTicksDiv = 15
    xticks = [x for x in data.columns.values]
    keptticks = xticks[::int(len(xticks)/xTicksDiv)]
    xticks = ['' for _ in xticks]
    xticks[::int(len(xticks)/xTicksDiv)] = keptticks
    g = sns.heatmap(data.loc[sleepValue].reshape(1,-1))
    g.set_xticklabels(xticks, rotation=45)
    g.set_yticklabels([])
    g.set_ylabel(sleepStats.SLEEP_VALUES[sleepValue])
    sns.plt.show()

def plotCorrelation(stats):
    columnsToDrop = ['sleep_interval_max_len', 'sleep_interval_min_len',
                     'sleep_interval_avg_len', 'sleep_inefficiency',
                     'sleep_hours', 'total_hours']

    stats = stats.drop(columnsToDrop, axis=1)

    g = sns.PairGrid(stats)
    def corrfunc(x, y, **kws):
        r, p = scipystats.pearsonr(x, y)
        ax = plt.gca()
        ax.annotate("r = {:.2f}".format(r),xy=(.1, .9), xycoords=ax.transAxes)
        #ax.annotate("p = {:.2f}".format(p),xy=(.2, .8), xycoords=ax.transAxes)
        if p>0.04:
            ax.patch.set_alpha(0.1)

    g.map_upper(plt.scatter)
    g.map_diag(plt.hist)
    g.map_lower(sns.kdeplot, cmap="Blues_d")
    g.map_upper(corrfunc)
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