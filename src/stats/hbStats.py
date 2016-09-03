import pandas as pd

NAME_VAL_COL = "value"
NAME_DT_COL = "datetime"

def basicStats(hbData):
    return hbData.describe()

def groupByBasicStats(groupByFun, data, indexName=None):
    hbData = data.groupby(groupByFun)

    stats = {'count' : hbData[NAME_VAL_COL].count(),
        'mean' : hbData[NAME_VAL_COL].mean(),
        'min' : hbData[NAME_VAL_COL].min(),
        'max' : hbData[NAME_VAL_COL].max(),
        'std' : hbData[NAME_VAL_COL].std()
             }

    df = pd.DataFrame.from_dict(stats)

    if indexName:
        df.index.name = indexName

    return df.reset_index()

def getMaxValues(data, n):
    return data.nlargest(n, NAME_VAL_COL)

def getMinValues(data, n):
    return data.nsmallest(n, NAME_VAL_COL)