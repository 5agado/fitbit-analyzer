import unittest

from resources import RESOURCE_PATH
from stats import sleepStats
from util import utils

class SleepStatsTestCase(unittest.TestCase):
    def test_firstMinuteAsleep(self):
        filepath =  RESOURCE_PATH + "\\unittest\\test_sleepStats.csv"
        data = utils.loadIntradayData(filepath)
        firstMinuteAsleep = sleepStats.getFirstMinuteAsleep(data)
        self.assertEqual(firstMinuteAsleep, 8)

        firstMinuteAsleep = sleepStats.getFirstMinuteAsleep(data, 10)
        self.assertEqual(firstMinuteAsleep, 8)

        firstMinuteAsleep = sleepStats.getFirstMinuteAsleep(data, 11)
        self.assertEqual(firstMinuteAsleep, 19)

        firstMinuteAsleep = sleepStats.getFirstMinuteAsleep(data, 500)
        self.assertEqual(firstMinuteAsleep, None)

if __name__ == '__main__':
    unittest.main()
