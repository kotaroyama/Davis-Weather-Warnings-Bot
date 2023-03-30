from datetime import datetime
from os import environ, remove

import boto3
from pytz import timezone
import requests
import tweepy

from create_temp import create_html


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


def upload_html_to_s3(html_file):
    # Upload the file
    s3_client = boto3.client(
        's3',
        region_name='us-west-1',
        aws_access_key_id=environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=environ['AWS_SECRET_ACCESS_KEY']
    )
    s3_client.upload_file(
        f'templates/{html_file}',
        'davis-weather-bot-images',
        html_file,
        ExtraArgs={
            'ContentType': "text/html",
            'ACL':'public-read',
        }
    )


def tweet_weather(weather_warnings, city, state):
    """Tweets out the current active warnings"""
    api = twitter_api()

    # Current time to be added to the tweet
    # time_now = datetime.now()
    time_now = datetime.now(timezone('US/Pacific'))
    time_formatted = time_now.strftime("%I:%M %p %b %d %Y")
   
    # Check if there is an active warning
    if weather_warnings['active']:
        # Create an html file to be converted to an image
        create_html(weather_warnings)
        html_file = 'index.html'

        # Upload the html to S3 bucket and get the URL
        upload_html_to_s3(html_file)

        # Tweet the image along with a message
        tweet = f'{time_formatted}\n\nActive warning in {city}, {state}.\n\nhttps://davis-weather-bot-images.s3.us-west-1.amazonaws.com/index.html'
        api.update_status(tweet)

        print('Tweeted successfully')
"""
    else:
        # Tweet with empty message
        tweet = f'{time_formatted}\n\nNo Alerts Found.'
        api.update_status(tweet)
"""
