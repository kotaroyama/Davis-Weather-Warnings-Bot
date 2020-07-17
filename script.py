"""Twitter Bot for Weather Alerts in Davis, California

@DavisWeatherBot
Asks for an update every minute from National Weather API (weather.gov).

Written by Kotaro Yama (kotaro.h.yama@gmail.com)"""

import time
import queue

import requests
import tweepy

import credentials

def get_lat_and_long(city, state):
    """Using Google's Geoencoding API, given a city name, return an array of latitude and longitude"""
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={city},+{state}&key={credentials.GEO_API_KEY}'
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

    # If there is/are active warning(s)
    if r.json()['features']:
        warnings = r.json()['features']
    else:
        print("No warnings")

    # Array of Warnings to be returned
    warnings_legible = [] 

    # Parse Warnings 
    for warning in warnings:
        counties_affected = warning['properties']['areaDesc']  
        headline = warning['properties']['headline']
        sender_name = warning['properties']['senderName'] 
        description = warning['properties']['description']
        
        # Append the formatted warning to the list
        warnings_legible.append({
            "counties_affected": counties_affected,
            "headline": headline,
            "sender_name": sender_name,
            "description": description
        })

    return warnings_legible

def tweet_weather(weather_warnings):
    pass

def main():
    # City and state for lat and long
    #   City - use '+' for space
    #   State: use two char ANSI abbreviations   
    city = "Minneapolis"
    state = "MN"
    location = get_lat_and_long(city, state)

    weather_warnings = get_weather_warning(location['latitude'], location['longitude'])

if __name__ == "__main__":
    main()
