# Fitbit Analyzer
Analyzer and statistics generator for Fitbit data like sleep, steps count and heart rate. Check out also [my related introductory article](https://medium.com/@5agado/a-quest-for-better-sleep-with-fitbit-data-analysis-5f10b3f548a#.inflxkcln).

## Usage
*requirements.txt* is the exported environment file. See [here](http://conda.pydata.org/docs/using/envs.html#share-an-environment) for a guide on how to manage Conda environments.

The [Sleep Dashboard notebook](Sleep%20Dashboard.ipynb) can provide a quick way to explore your sleep data. See [related article](https://medium.com/towards-data-science/interactive-visualizations-in-jupyter-notebook-3be02ab2b8cd) and [video](https://www.youtube.com/watch?v=FYnM84TgzZU). I am currently working on notebooks for the other measures, so all feedback is welcome.

## Scraping Info
I am here giving some info about scraping Fitbit data, but notice that scraper code is not provided in this repository.

I [my article](https://medium.com/@5agado/a-quest-for-better-sleep-with-fitbit-data-analysis-5f10b3f548a#.xhzjsb6wz) I complained about the issue related with obtaining all my personal Fitbit data. There is no immediate click-and-download way to get all the data you interested in, and what I did when I started this analysis of mine was to rely on some website-scraping Python code. The most recent version of working code I was able to find was [the one of Andrew](https://github.com/andrewjw/python-fitbit). 

After I had played a bit with the data, I wanted to improve such code, for example by using the Session object from Requests, and adding the scraping of heartbeat data. Is nice playing a bit with the basics of such mechanisms, but I soon became frustrated trying to replicate the graph data call of the Fitbit website. I searched again for easier and better solutions, and I ended up [on this Fitbit community post](https://community.fitbit.com/t5/Web-API/Intraday-data-now-immediately-available-to-personal-apps/td-p/1014524), explaining a simplified way for a user to collect all his data via the official APIs. Briefly speaking you have to create a Fitbit app on the website, configure it as described in the previous link and implement a OAuth flow in order to obtain the access tokens needed for the API calls.  
If you use Python, I suggest to rely on [the official python implementation of the Fitbit API](http://python-fitbit.readthedocs.io/en/latest/index.html#fitbit.Fitbit.intraday_time_series) and give a look [here](http://blog.mr-but-dr.xyz/en/programming/fitbit-python-heartrate-howto/) for a clear explanation on what needs to be done to have all setup and running.
I have to admit that this ended up to be easier and cleaner that the previous scraper solution, still, you need to keep a couple of things in mind:

1. You have to write some code to clean the JSON data returned by the API, and extract the info relevant to you
2. Seems like the API have a limit of 150 calls per hour, so you might need to repeat the operation several times depending on how much and what data you need

## Data Format
All this said, in this repository I am not sharing the scraper code, but in the *util* folder you can find some code for loading sleep, heartbeat and steps data as provided by the previously mentioned procedure. 
For the data-dump folder I have one folder per year, and then one sub-folder for each day, in which the different files are generated (e.g. *sleep.json*, *steps.json*).

Example:
```
├───2016
│   ├───2016-01-01
│   │       sleep.json
│   │       steps.json
│   │
│   └───2016-01-02
│           heartbeat.json
│
└───2017
    └───2017-01-11
            calories.json
            distance.json
            elevation.json
            floors.json
            heartbeat.json
            sleep.json
            steps.json
```

## Sleep Stats
Sleep values are mapped like this: 0=none (no measure taken), 1=sleeping, 2=restless, 3=awake.

* **Basic Stats** (sleep values count, sleep efficiency, hours of sleep, total minutes in bed, N max-values for each stat)
* **Timing Stats** (first minute asleep, to bed time, wake up time, sleep interval min/max length)
* **Intervals Stats** for each day all the sleep intervals lengths
* **Intraday Stats** minute to minute report for each day, for the specified sleep values. Total value count, with normalization and centering on specific time.


## Heart Rate Stats
* **Basic Stats** (count, mean, min, max, std) values for the entire dataset, or for aggregated subsets. Common aggregation features are date, year, month, day, day of week and hour  
* **Daily Stats** plotting of average heart-rate by day, month, year, weekday
* **Min/Max Values** get the N min or max heartbeat values in the dataset

## Steps Stats
* **Daily Count** steps count per day

**NEW**
## Combined Stats
* **Correlation** correlation coefficient between heterogeneous stats (e.g. steps and sleep)
* **Combined TOGGL and heart-rate stats** explore relations between Toggl activities and projects and heart-rate

## TODO
* provide your sleep analysis (devTesting notebook) in an automated and generic way
* toggl data exploratory notebook
* Moving average sleep (days for achieving flatness)
* correlation between constant exercise/running and decreased heart-rate
* derive sleep-states (REM/NREM) stats (e.g. identify, how long in each) from basic ones, or via correlation with heartbeat (as for now doesn't seem to be feasible actual ECG is still the more proper option)

## License

Released under version 2.0 of the [Apache License].

[Apache license]: http://www.apache.org/licenses/LICENSE-2.0
[my related article]: https://medium.com/@5agado/conversation-analyzer-baa80c566d7b#.w20u1gltf