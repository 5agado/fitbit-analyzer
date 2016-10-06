import pandas as pd
import numpy as np

NAME_VAL_COL = "value"
NAME_DT_COL = "datetime"

def groupAndSumByDate(stepsData):
    data = stepsData
    if isinstance(stepsData, list):
        data = pd.concat(stepsData, ignore_index=True)
    res = data.groupby(data[NAME_DT_COL].dt.date)[NAME_VAL_COL].sum()
    return res