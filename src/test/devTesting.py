import argparse
import sys
import configparser
import logging
import time
import os

import pandas as pd
import numpy as np
import seaborn as sns

from resources import RESOURCE_PATH
from stats import sleepStats
from util import utils
from util import plotting as mplot

def main(_):
    parser = argparse.ArgumentParser(description='Fitbit Analyzer')
    parser.add_argument('-f', metavar='dataFolder', dest='dataFolder', required=True)

    args = parser.parse_args()

    #first specify data folder, if used scraper I used, format is each year has it's one
    #folder
    #TODO recursive folder search
    #it really depends on how you got your data, and how is it saved, for my case, using [missing]
    #I got one folder per year, and for each year a folder for each day, in which different files
    #are saved, like "sleep.txt"

    #get the data
    dataFolder = args.dataFolder
    filepath =  RESOURCE_PATH + "\\unittest\\test_sleepStats.csv"

    #generate stats

    #save them to file, so we can reuse the results without recomputing every time

    #load saved stats
    stats = pd.read_csv(dataFolder + "//stats.csv", parse_dates=[0])

    #plot
    #todo, use facetgrid??, write down considerations

    mplot.plotPreliminaryStats(stats)
    mplot.plotWeekdayStats(stats)
    mplot.plotMonthlyStats(stats)
    #todo use smoothing for this one, try interpolation for missing values
    #better print just one or two stats
    #there should be no mean
    mplot.plotDailyStats(stats)

    stats = pd.read_csv(dataFolder + "//intradayStats.csv")
    mplot.plotSleepValueHeatmap(stats)

    return

if __name__ == "__main__":
    main(sys.argv[1:])