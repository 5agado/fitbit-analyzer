import argparse
import datetime
import sys
import os
import numpy as np

import plotly
from plotly.graph_objs import Scatter, Layout
import plotly.plotly as py
import plotly.graph_objs as go


import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from stats import sleepStats


from util import utils

from resources import RESOURCE_PATH
from util import plotting as mplot


def main(_):
    parser = argparse.ArgumentParser(description='Fitbit Analyzer')
    parser.add_argument('-f', metavar='dataFolder', dest='dataFolder', required=True)

    args = parser.parse_args()
    dataFolder = args.dataFolder

    trace = go.Scatter3d(
        x=pd.Series(data.columns.values), y=pd.Series(np.ones(len(data.columns.values))), z=data.loc[1],
        marker=dict(
            size=4,
            color=data.loc[1].reshape(1,-1),
            colorscale='Viridis',
        ),
        line=dict(
            color='#1f77b4',
            width=1
        )
    )

    data = [trace]

    layout = go.Layout(
        width=800,
        height=700,
        autosize=False,
        title='Iris dataset',
        scene=dict(
            xaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            yaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            zaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            camera=dict(
                up=dict(
                    x=0,
                    y=0,
                    z=1
                ),
                eye=dict(
                    x=-1.7428,
                    y=1.0707,
                    z=0.7100,
                )
            ),
            aspectratio = dict( x=1, y=1, z=0.7 ),
            aspectmode = 'manual'
        ),
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig)

    #todo, use facetgrid??, write down considerations
    return

if __name__ == "__main__":
    main(sys.argv[1:])

def correlateSleepAndHb(sleepData, hbData):
    corrData = []
    for i in range(len(sleepData)):
        if i<len(sleepData):
            hb = pd.concat([hbData[i],hbData[i+1]])
        else:
            hb = hbData[i]
        corrData.append(pd.merge(sleepData[i],hb,on='datetime', how='inner',suffixes=('_sleep', '_hb') ))

    fs = []
    for d in corrData:
        #print(d)
        #print(d.groupby('value_sleep').mean())
        #d.drop('datetime', inplace=True, axis=1)
        #cols_to_norm = ['value_hb','value_sleep']
        #d['value_hb'] = d['value_hb'].apply(lambda x: ((x - x.mean()) / (x.max() - x.min())))
        #d['value_hb'] = (d['value_hb']-d['value_hb'].mean())/(d['value_hb'].max()-d['value_hb'].min())+1
        #print(d)
        #print(d['value_hb'])
        #r, p = scipystats.pearsonr(d['value_hb'].values, d['value_sleep'].values)
        #print("r = {:.2f}".format(r))
        #d['hour'] = d['datetime'].dt.hour
        f = d.groupby('hour', as_index=False).mean()
        #sns.boxplot(x="hour", y="value_hb", data=f)
        #g.set(xticklabels=[])
        #plt.show()
        #f.plot()
        fs.append(f)
    res = pd.concat(fs)
    print(res)