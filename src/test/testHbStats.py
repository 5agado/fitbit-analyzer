import unittest

from src.resources import RESOURCE_PATH
from src.stats import hbStats
from src.util import utils
import pandas as pd

class HbStatsTestCase(unittest.TestCase):
    def test_basicStats(self):
        filepath =  RESOURCE_PATH + "\\unittest\\test_hb_basic01.csv"
        data = utils.loadIntradayData(filepath).set_index('datetime')
        stats = hbStats.groupByBasicStats(pd.TimeGrouper(freq='d'), data)

        self.assertEqual(stats.iloc[0]['count'], 16)
        self.assertEqual(stats.iloc[0]['max'], 70)
        self.assertEqual(stats.iloc[0]['min'], 50)
        self.assertEqual(stats.iloc[0]['mean'], 60)

    def test_minMax(self):
        filepath =  RESOURCE_PATH + "\\unittest\\test_hb_basic01.csv"
        data = utils.loadIntradayData(filepath).set_index('datetime')
        stats = hbStats.getMaxValues(data, 2)

        self.assertEqual(stats.iloc[0].value, 70)
        self.assertEqual(stats.iloc[1].value, 60)

        stats = hbStats.getMinValues(data, 2)

        self.assertEqual(stats.iloc[0].value, 50)
        self.assertEqual(stats.iloc[1].value, 60)

if __name__ == '__main__':
    unittest.main()
