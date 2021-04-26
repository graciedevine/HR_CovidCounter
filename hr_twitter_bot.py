# import requests
# import tweepy
# import textwrap
# from datetime import datetime, timedelta

# # Make an API call and store the response.
# url = 'https://data.virginia.gov/resource/bre9-aqqr.json'
# response = requests.get(url)

# # Store an API response in a variable.
# data_set = response.json()


import json
with open('test.json') as f:
    data_set = json.load(f)


# Create an empty dictionary; localities from this list will be inserted
data = dict()
localities = ['Chesapeake', 'Hampton', 'Newport News', 'Norfolk', 'Portsmouth', 'Suffolk', 'Virginia Beach']

# Extract locality from the json and add entry to dictionary
for entry in data_set:
    locality = entry['locality']
    if locality in localities and locality not in data:
        data[locality] = entry

def total_cases(): 
    """Total number of confirmed cases in Hampton Roads."""

    # Extract total_cases from field; cast to int and then sum everything
    for r in data.values():
        total_cases = sum([int(i['total_cases']) for i in data.values()])
        # print('Confirmed Cases: ' + f"{total_cases:,}")
        break


# def hospitalizations():
#     """Total number of hospitalizations in Hampton Roads."""

    # Extract hospitalizations from field; cast to int and then sum everything
    for r in data.values():
        total_hosp = sum([int(i['hospitalizations']) for i in data.values()])
        # print('Hospitalizations: ' + f"{total_hosp:,}")
        break


# def total_deaths():
#     """Total number of deaths in Hampton Roads."""

    # Extract deaths from field; cast to int and then sum everything
    for r in data.values():
        total_deaths = sum([int(i['deaths']) for i in data.values()])
        # print('Deaths: ' + f"{total_deaths:,}")
        break


def write_tweet(data):
    """Uses daily COVID-19 data to write/format tweet"""

    # Convert the datetime into a string
    yesterday = datetime.today().date() - timedelta(days=1)
    yesterday_str = yesterday.strftime("%b %d")

    # Format the tweet
    tweet = textwrap.dedent(f'''
        Total Cases on {yesterday_str}: {data["total_cases"]:,}
        Hospitalized on {yesterday_str}: {data["hospitalized"]:,}
        Deaths on {yesterday_str}: {data['deaths']:,}

         Data taken from: https://www.vdh.virginia.gov/coronavirus/
    ''').strip()
    return tweet

data = total_cases()
# hospitalizations()
# total_deaths()






def send_tweet():
     # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create API object
    api = tweepy.API(auth)

    # Test credentials
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    
    # Upload image of graph to tweet
    # image = api.media_upload('graph.png')
    
    # Create tweet
    api.update_status(text)
    # (text, media_ids=[image.media_id, ])


# def graph():
#     """Graphs the 14-day moving average and number of confirmed cases."""
