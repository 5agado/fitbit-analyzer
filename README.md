# Fitbit Analyzer
Analyzer and statistics generator for Fitbit data like sleep, steps count and heart rate. Check out also [my related introductory article](https://medium.com/@5agado/a-quest-for-better-sleep-with-fitbit-data-analysis-5f10b3f548a#.inflxkcln).

Includes OAuth 2.0 **scraper** to download personal Fitbit data using the [Fitbit API Python Client Implementation](http://python-fitbit.readthedocs.io/en/latest/).

## Usage
Run

     python setup.py install

You will then be able to run the scraper via

    fitbit-scraper --id <your_client_id> --secret <your_client_secret> --out dump/destination/folder/path

The client-id and client-secret can be obtained by creating a Fitbit app on the official website. The scraper will than take care to download all data to the given folder, avoiding to re-download data already present (apart for the last present day, which will be re-scraped to avoid missing entries). See `fitbit-scraper --help` for a detailed usage description.

### Data Format
In the *util* folder you can find some code for loading sleep, heartbeat and steps data as dumped by the scraper script.
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

## Analyzer and Stats
Compared to basic scraping this phase has more dependencies; see the *requirements.txt* file and [here](http://conda.pydata.org/docs/using/envs.html#share-an-environment) for a guide on how to manage environments in Conda.

The [Sleep Dashboard notebook](Sleep%20Dashboard.ipynb) can provide a quick way to explore your sleep data. See [related article](https://medium.com/towards-data-science/interactive-visualizations-in-jupyter-notebook-3be02ab2b8cd) and [video](https://www.youtube.com/watch?v=FYnM84TgzZU). I am currently working on notebooks for the other measures, so all feedback is welcome.


### Sleep Stats
Sleep values are mapped like this: 0=none (no measure taken), 1=sleeping, 2=restless, 3=awake.

* **Basic Stats** (sleep values count, sleep efficiency, hours of sleep, total minutes in bed, N max-values for each stat)
* **Timing Stats** (first minute asleep, to bed time, wake up time, sleep interval min/max length)
* **Intervals Stats** for each day all the sleep intervals lengths
* **Intraday Stats** minute to minute report for each day, for the specified sleep values. Total value count, with normalization and centering on specific time.


### Heart Rate Stats
* **Basic Stats** (count, mean, min, max, std) values for the entire dataset, or for aggregated subsets. Common aggregation features are date, year, month, day, day of week and hour  
* **Daily Stats** plotting of average heart-rate by day, month, year, weekday
* **Min/Max Values** get the N min or max heartbeat values in the dataset

### Steps Stats
* **Daily Count** steps count per day

**NEW**
### Combined Stats
* **Correlation** correlation coefficient between heterogeneous stats (e.g. steps and sleep)
* **Combined TOGGL and heart-rate stats** explore relations between Toggl activities and projects and heart-rate

## TODO
* Toggl data exploratory notebook
* moving average sleep (days for achieving flatness)
* correlation between constant exercise/running and decreased heart-rate
* formal verification of causality (e.g. good sleep causes to walk, or walk cause good sleep)
* derive sleep-states (REM/NREM) stats (e.g. identify, how long in each) from basic ones, or via correlation with heartbeat (as for now doesn't seem to be feasible actual ECG is still the more proper option)
* max HR and zones (% of MHR)

## License

Released under version 2.0 of the [Apache License].

[Apache license]: http://www.apache.org/licenses/LICENSE-2.0
[my related article]: https://medium.com/@5agado/conversation-analyzer-baa80c566d7b#.w20u1gltf