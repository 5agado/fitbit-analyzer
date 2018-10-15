import unittest
import pandas as pd

from src.resources import RESOURCE_PATH
from src.stats import sleepStats
from src.util import utils
from src.util import plotting as mplot

class SleepStatsTestCase(unittest.TestCase):
    def test_plottingOnBasicStats(self):
        filepath =  RESOURCE_PATH + "\\unittest\\test_sleep_basic01.csv"
        data1 = utils.loadIntradayData(filepath)
        filepath =  RESOURCE_PATH + "\\unittest\\test_sleep_basic02.csv"
        data2 = utils.loadIntradayData(filepath)
        stats = sleepStats.generateStatsFrom([data1, data2],
                                             sleepStats.STATS_NAME_BASIC_AND_TIMING).reset_index()
        stats['date'] = pd.to_datetime(stats['date'])

        mplot.plotYearAndMonthStatsSleep(stats)
        mplot.plotPreliminaryStats(stats)
        mplot.plotWeekdayStatsSleep(stats)
        mplot.plotDailyStatsSleep(stats)
        mplot.plotMonthlyStatsSleep(stats)


    def test_plottingOnIntradayStats(self):
        filepath =  RESOURCE_PATH + "\\unittest\\test_sleep_basic01.csv"
        data1 = utils.loadIntradayData(filepath)
        filepath =  RESOURCE_PATH + "\\unittest\\test_sleep_basic02.csv"
        data2 = utils.loadIntradayData(filepath)
        stats = sleepStats.generateStatsFrom([data1, data2],
                                             sleepStats.STATS_NAME_INTRADAY)

        data = stats.apply(pd.value_counts)
        mplot.plotSleepValueHeatmap(data, sleepValue=1)

if __name__ == '__main__':
    unittest.main()
