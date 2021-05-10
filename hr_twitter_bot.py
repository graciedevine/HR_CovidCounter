import json
import tweepy
import requests
import pandas as pd
import matplotlib.pyplot as plt
import textwrap
from datetime import datetime
from twitter_keys import (
    consumer_key,
    consumer_key_secret,
    access_token,
    access_token_secret,
)

URL = "https://data.virginia.gov/resource/bre9-aqqr.json"
LOCALITIES = [
    "Chesapeake",
    "Hampton",
    "Newport News",
    "Norfolk",
    "Portsmouth",
    "Suffolk",
    "Virginia Beach",
]

TOTAL = "total_cases"
HOSP = "hospitalizations"
DEATH = "deaths"
RDATE = "report_date"


def get_raw_data(from_file=False):
    if from_file:
        with open("test.json") as f:
            return json.load(f)

    response = requests.get(URL)
    return response.json()


def extract_summary_info(raw_data):
    """Total number of confirmed cases in Hampton Roads."""
    data = dict()
    for entry in raw_data:
        locality = entry["locality"]
        if locality in LOCALITIES and locality not in data:
            data[locality] = entry

    fields = [TOTAL, HOSP, DEATH]
    return {
        field: sum([int(info[field]) for locality, info in data.items()])
        for field in fields
    }


def tweet_text(data):
    """Uses daily COVID-19 data to write/format tweet"""

    today = datetime.today().date()
    today_str = today.strftime("%b %d")

    tweet = textwrap.dedent(
        f"""
        Total Cases as of {today_str}: {data[TOTAL]:,}
        Hospitalized as of {today_str}: {data[HOSP]:,}
        Deaths as of {today_str}: {data[DEATH]:,}

        Data taken from: https://www.vdh.virginia.gov/coronavirus/
        *Bot runs daily at noon; VDH data update time and dates vary.
    """
    ).strip()
    return tweet


def graph_moving_average(data):

    daily_data = pd.DataFrame(data)
    for col in [DEATH, HOSP, TOTAL]:
        daily_data[col] = pd.to_numeric(daily_data[col])

    daily_data[RDATE] = pd.to_datetime(daily_data[RDATE])
    daily_data = daily_data[daily_data.locality.isin(LOCALITIES)].groupby(RDATE).sum()

    daily_data["New Positive Cases"] = daily_data["total_cases"]
    daily_data["New 14-day Moving Average"] = (
        daily_data["New Positive Cases"].rolling(7).mean()
    )
    daily_data[["New Positive Cases", "New 14-day Moving Average"]].plot()

    plt.title("DAILY POSITIVE COVID-19 CASES IN VIRGINIA")
    plt.ylabel("Increase in Positive Cases from Previous Day")
    plt.xlabel("Dates (last 120 days")
    plt.show()


def send_tweet(text):
    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    # image = api.media_upload('graph.png')

    api.update_status(text)
    # (text, media_ids=[image.media_id, ])


if __name__ == "__main__":
    raw_data = get_raw_data()
    data = extract_summary_info(raw_data=raw_data)
    text = tweet_text(data)
    send_tweet(text)
    graph_moving_average(raw_data)
    print(text)
