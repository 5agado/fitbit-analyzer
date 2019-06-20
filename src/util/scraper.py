import datetime
import json
import sys
import argparse
from pathlib import Path

import fitbit
from src.util import logger
from src.util import gather_keys_oauth2 as Oauth2


def dumpToFile(data_type, dumpDir: Path, date, data):
    directory = dumpDir / str(date.year) / str(date)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "{}.json".format(data_type)).open(mode='w') as f:
        f.write(json.dumps(data, indent=True))


def previouslyDumped(dumpDir: Path, date):
    return (dumpDir / str(date.year) / str(date)).is_dir()


def dumpDay(client, dumpDir: Path, date):
    steps_data = client.intraday_time_series('activities/steps', date)
    intradayData = steps_data['activities-steps-intraday']['dataset']
    if not intradayData:
        logger.info("No {} measures for {}. Skipping the rest too".format('steps', date.split('\\')[-1]))
        return None

    dumpToFile("steps", dumpDir, date, steps_data)
    dumpToFile("sleep", dumpDir, date, client.get_sleep(date))
    dumpToFile("calories", dumpDir, date, client.intraday_time_series('activities/calories', date))
    dumpToFile("distance", dumpDir, date, client.intraday_time_series('activities/distance', date))
    dumpToFile("floors", dumpDir, date, client.intraday_time_series('activities/floors', date))
    dumpToFile("elevation", dumpDir, date, client.intraday_time_series('activities/elevation', date))
    dumpToFile("heartbeat", dumpDir, date, client.intraday_time_series('activities/heart', date))


def scrapeFromDateOnward(startDate, dumpDir: Path, client):
    date = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    todayDate = datetime.date.today()
    while previouslyDumped(dumpDir, date):
        logger.info("Already scraped {}".format(datetime.datetime.strftime(date, "%Y-%m-%d")))
        date += datetime.timedelta(days=1)

    date -= datetime.timedelta(days=1)
    logger.info("Will RE-Scrape data for {}".format(datetime.datetime.strftime(date, "%Y-%m-%d")))
    while date < todayDate:
        logger.info("Scraping data for {}".format(datetime.datetime.strftime(date, "%Y-%m-%d")))
        dumpDay(client, dumpDir, date)
        date += datetime.timedelta(days=1)


def scrapeFromTodayAndBackward(dumpDir: Path, client, limit, stop_if_already_dumped=True):
    # dumping
    count = 1
    date = datetime.date.today()
    while count < limit:
        if previouslyDumped(dumpDir, date):
            logger.info("Already scraped {}".format(date.isoformat()))
            if stop_if_already_dumped:
                print("Stopping the scraping")
                break
            date -= datetime.timedelta(days=1)
            continue
        logger.info("Scraping data for {}".format(date.isoformat()))
        dumpDay(client, dumpDir, date)
        date -= datetime.timedelta(days=1)
        count += 1
    dumpDay(client, dumpDir, date)


def main(_=None):
    parser = argparse.ArgumentParser(description='Fitbit Scraper')
    parser.add_argument('--id', metavar='clientId', dest='clientId', required=True,
                        help="client-id of your Fitbit app")
    parser.add_argument('--secret', metavar='clientSecret', dest='clientSecret', required=True,
                        help="client-secret of your Fitbit app")
    parser.add_argument('--out', metavar='outDir', dest='outDir', required=True,
                        help="output data destination folder")
    parser.add_argument('--start', dest='startDate', default='2016-01-01',
                        help="Date from which to start the forward scraping. Defaults to 2016-01-01")
    #parser.add_argument('--limit', type=int, dest='limit', default=400,
    #                    help="maximum number of days to scrape")

    args = parser.parse_args()
    clientId = args.clientId
    clientSecret = args.clientSecret
    dumpDir = Path(args.outDir)
    startDate = args.startDate
    #limit = args.limit

    server = Oauth2.OAuth2Server(clientId, clientSecret)
    server.browser_authorize()

    ACCESS_TOKEN = server.oauth.session.token['access_token']
    REFRESH_TOKEN = server.oauth.session.token['refresh_token']

    client = fitbit.Fitbit(clientId, clientSecret, oauth2=True,
                           access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

    scrapeFromDateOnward(startDate, dumpDir, client)


if __name__ == "__main__":
    main(sys.argv[1:])