import json
from pprint import pprint
import sys
import unittest

sys.path.insert(1, '..')
from script import get_weather_warning, get_lat_and_long

class TestWeatherWarnings(unittest.TestCase):

    def test_location_point(self):
        LAT = 38.5449
        LONG = -121.7405
        city = 'Davis'
        state = 'CA'
        point = get_lat_and_long(city, state) 

        self.assertAlmostEqual(LAT, float(point['latitude']))
        self.assertAlmostEqual(LONG, float(point['longitude']))


    def test_legible_weather_data(self):
        city = 'Davis'
        state = 'CA'
        point = get_lat_and_long(city, state) 
        weather_data = get_weather_warning(point['latitude'], point['longitude'])

        pprint(weather_data)

        # export it to JSON
        with open('../data/sample.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)

        self.assertIsNotNone(weather_data)

if __name__ == '__main__':
    unittest.main()
