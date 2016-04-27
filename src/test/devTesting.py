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

def main(_):
    parser = argparse.ArgumentParser(description='Fitbit Analyzer')
    parser.add_argument('-f', metavar='dataFolder', dest='dataFolder', required=True)

    args = parser.parse_args()
    dataFolder = args.dataFolder
    filepath =  RESOURCE_PATH + "\\unittest\\test_sleepStats.csv"

    return

if __name__ == "__main__":
    main(sys.argv[1:])