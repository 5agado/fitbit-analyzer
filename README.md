# Fitbit Analyzer
Analyzer and statistics generator for Fitbit data like sleep, steps count and heart rate. If interested, check out also [my related article](https://medium.com/@5agado/a-quest-for-better-sleep-with-fitbit-data-analysis-5f10b3f548a#.inflxkcln).

##Usage
*requirements.txt* is the exported environment file. See [here](http://conda.pydata.org/docs/using/envs.html#share-an-environment) for a guide on how to manage Conda environments.

The project is still a WIP, now just focusing on sleep measures.   
I used [this code](https://github.com/andrewjw/python-fitbit) to scrape all my data. It creates one folder per year, and then one sub-folder for each day, in which the different files are generated (e.g. *sleep.txt*, *steps.txt*).


##TODO
* better and more general folder search for data files
* proper testing of current sleep stats
* possibility of rewriting scraper using Requests

## License

Released under version 2.0 of the [Apache License].

[Apache license]: http://www.apache.org/licenses/LICENSE-2.0
[my related article]: https://medium.com/@5agado/conversation-analyzer-baa80c566d7b#.w20u1gltf