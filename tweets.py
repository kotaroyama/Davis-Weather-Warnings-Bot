from collections import deque
from datetime import datetime
from os import environ

import tweepy

from create_temp import create_html, html_to_img


def twitter_api():
    # Twitter credentials
    CONSUMER_KEY = environ['CONSUMER_KEY']
    CONSUMER_SECRET = environ['CONSUMER_SECRET']
    ACCESS_KEY = environ['ACCESS_KEY']
    ACCESS_SECRET = environ['ACCESS_SECRET']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api


def tweet_weather(weather_warnings):
    """Tweets out the current active warnings"""
    api = twitter_api()
   
    # Check if there is an active warning
    if weather_warnings['active']:
        # Create an html file to be converted to an image
        create_html(weather_warnings)    

        # Convert the html file to an image
        html_file = 'templates/alert.html'
        image_file = 'templates/out.jpg'
        html_to_img(html_file)
        
        # Tweet the image along with a message
        message = 'Active warning!'
        api.update_with_media(image_file, status=message)
    else:
        # Tweet with empty message
        tweet = 'Good for now... Go Aggies!'
        api.update_status(tweet)
