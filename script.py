"""Twitter Bot for Weather Alerts in Davis, California

@DavisWeatherBot
Asks for an update every minute from National Weather API (weather.gov).

Written by Kotaro Yama (kotaro.h.yama@gmail.com)"""

from collections import deque
from datetime import datetime
from os import environ
import time

import requests
import tweepy


def get_lat_and_long(city, state):
    """Using Google's Geoencoding API, given a city name, return an array of latitude and longitude"""
    GEO_API_KEY = environ['GEO_API_KEY']
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={city},+{state}&key={GEO_API_KEY}'
    r = requests.get(url)
    geo_data = r.json()

    # Extract lat and long from the JSON
    latitude = str(geo_data['results'][0]['geometry']['location']['lat'])
    longitude = str(geo_data['results'][0]['geometry']['location']['lng'])
    
    # Dictionary with coordinates
    coordinates = {'latitude': latitude[:-3], 'longitude': longitude[:-3]}

    return coordinates
    
def get_weather_warning(latitude, longitude):
    """Using National Weather Service API (weather.gov), get the weather
    warnings for the current area

    The function returns an object which contains a list of warnings. Each
    warning has a headline, counties affected, sender name, and description.
    """
    url = f'https://api.weather.gov/points/{latitude},{longitude}'
    r = requests.get(url)
    weather_data = r.json()

    # Extract Area Code and get the active weather warnings
    zone = weather_data['properties']['fireWeatherZone'][-6:]
    url = f"https://api.weather.gov/alerts/active/zone/{zone}"
    r = requests.get(url)

    warnings = []
    # Array of Warnings to be returned
    warnings_legible = [] 

    # If there is/are active warning(s)
    if r.json()['features']:
        warnings = r.json()['features']
        # Parse Warnings 
        for warning in warnings:
            counties_affected = warning['properties']['areaDesc']  
            headline = warning['properties']['headline']
            sender_name = warning['properties']['senderName'] 
            description = warning['properties']['description']
            
            # Append the formatted warning to the list
            warnings_legible.append({
                "counties_affected": counties_affected,
                "active": True,
                "headline": headline,
                "description": description
            })
    else:
        print("No warnings")
        warnings_legible.append({
            "active": False,
            "headline": "No active warnings.",
            "description": "N/A"
        })

    return warnings_legible[0]

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

    # Components of the tweet
    headline = weather_warnings['headline'] + '\n'
    description = weather_warnings['description']

    # Calculate the total number of characters in the tweet components
    #   Get the number of tweets (max: 280 characters each tweet)
    num_of_max = 280
    num_of_chars = len(headline) + len(description)
    num_of_tweets = int(num_of_chars / num_of_max)

    # Additional tweet for remainders
    if num_of_chars % num_of_max:
        num_of_tweets += 1

    # Prepare tweets
    #   Tweet start with "Current time: hh:mm AM/PM on MM/DD/YYYY"
    #   Turn the description string into a queue split into words
    current_time = "(Update) " + datetime.utcnow().strftime("%I:%M %p %b %d %Y") + " (UTC)"
    description_queue = deque(description.split())

    # Initialize the tweets list
    tweets = [None] * num_of_tweets
    tweets[0] = current_time + '\n\n'
    tweets[0] += headline + '\n\n'

    if weather_warnings['active']:
        # Each tweet has a maximum of 280 characters
        #   If the description exceeds that, it's split into multiple tweets
        #   As you add words into tweets, pop the queue 
        for i in range(0, num_of_tweets):
            # If it's not the first tweet, then add "..."
            if i != 0:
                tweets[i] = '...'

            while description_queue:
                # Add '...' at the end if the description continues onto next tweet
                if tweets[i] and len(tweets[i]) + len(description_queue[0]) > (num_of_max - 3):
                    tweets[i] += '...'
                    break
                elif tweets[i]:
                    tweets[i] += description_queue.popleft()
                    tweets[i] += ' '
                else:
                    tweets[i] += description_queue.popleft()
                    tweets[i] += ' '
    else:
        tweets[0] += "Good for now... Go Aggies!"

    # Tweets using Tweepy API
    for tweet in tweets:
        api.update_status(tweet)

def main():
    # City and state for lat and long
    #   City - use '+' for space
    #   State: use two char ANSI abbreviations   
    city = "Davis"
    state = "CA"
    location = get_lat_and_long(city, state)

    weather_warnings = get_weather_warning(location['latitude'], location['longitude'])

    # Run the bot every hour
    INTERVAL = 60 * 60
    while True:
        tweet_weather(weather_warnings)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
