import tweepy
import textwrap
import requests
import json
from datetime import datetime, timedelta
from twitter_keys import consumer_key, consumer_key_secret, access_token, access_token_secret

URL = 'https://data.virginia.gov/resource/bre9-aqqr.json'
LOCALITIES = ['Chesapeake', 'Hampton', 'Newport News', 'Norfolk', 'Portsmouth', 'Suffolk', 'Virginia Beach']

TOTAL = 'total_cases'
HOSP = 'hospitalizations'
DEATH = 'deaths'

def get_raw_data(from_file = False):
    if from_file:
        with open('test.json') as f:
            data_set = json.load(f)
    else:
        response = requests.get(URL)
        data_set = response.json()

    data = dict()
    for entry in data_set:
        locality = entry['locality']
        if locality in LOCALITIES and locality not in data:
            data[locality] = entry

    return data


def extract_key_info(data):
    """Total number of confirmed cases in Hampton Roads."""

    fields = [TOTAL, HOSP, DEATH]

    return {
        field: sum([
            int(info[field]) 
            for locality, info in data.items()
        ])
        for field in fields
    }

def tweet_text(data):
    """Uses daily COVID-19 data to write/format tweet"""

    yesterday = datetime.today().date() - timedelta(days=1)
    yesterday_str = yesterday.strftime("%b %d")

    tweet = textwrap.dedent(f'''
        Total Cases on {yesterday_str}: {data[TOTAL]:,}
        Hospitalized on {yesterday_str}: {data[HOSP]:,}
        Deaths on {yesterday_str}: {data[DEATH]:,}

         Data taken from: https://www.vdh.virginia.gov/coronavirus/
    ''').strip()
    return tweet


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

if __name__ == '__main__':
   data = get_raw_data()
   data = extract_key_info(data=data)
   text = tweet_text(data)
   send_tweet(text)
   print(text)