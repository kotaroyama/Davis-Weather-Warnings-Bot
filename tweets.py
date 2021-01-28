from collections import deque
from datetime import datetime
from os import environ

import tweepy

def tweet_weather(weather_warnings):
    """Tweets out the current active warnings"""

    # Twitter credentials
    CONSUMER_KEY = environ['CONSUMER_KEY']
    CONSUMER_SECRET = environ['CONSUMER_SECRET']
    ACCESS_KEY = environ['ACCESS_KEY']
    ACCESS_SECRET = environ['ACCESS_SECRET']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    if weather_warnings['active']:
        pass    
    else:
        tweets[0] += "Good for now... Go Aggies!"

    # Tweets using Tweepy API
    for tweet in tweets:
        api.update_status(tweet)
