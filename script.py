"""Twitter Bot for Weather Alerts in Davis, California

@DavisWeatherBot
Asks for an update every minute from National Weather API (weather.gov).

Written by Kotaro Yama (kotaro.h.yama@gmail.com)"""

from os import environ
import re
import time

import requests

from tweets import tweet_weather


def get_lat_and_long(city, state):
    """Using Google's Geoencoding API, given a city name, return an array of latitude and longitude"""
    GEO_API_KEY = environ['GEO_API_KEY']
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city},+{state}&key={GEO_API_KEY}"
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
    zone = weather_data['properties']['forecastZone'][-6:]
    url = f"https://api.weather.gov/alerts/active/zone/{zone}"
    r = requests.get(url)

    warnings = []
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
            "head": "No active warnings.",
            "description": "N/A"
        })
        weather_data = warnings_legible[0]
        return weather_data

    # regular expressions to extract head, place and the issuer
    m_head = re.search('.+?(?= issued)', warnings_legible[0]['headline'])
    m_where = re.search('(?<=issued ).+?(?= by)', warnings_legible[0]['headline'])
    m_by = re.search('(?<=by ).*', warnings_legible[0]['headline'])

    weather_data = {
        'active': warnings_legible[0]['active'],
        'head': m_head.group(0),
        'by': m_by.group(0),
        'where': warnings_legible[0]['counties_affected'],
        'when': m_where.group(0),
        'what': generate_what(warnings_legible[0]['description'])
    }

    return weather_data

def generate_what(description):
    # Generate organized 'what' description
    chunks = description.split('*')
    what = chunks[1][8:]
    return what

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
