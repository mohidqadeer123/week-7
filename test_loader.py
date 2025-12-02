import unittest
import pandas as pd
from loader import *

class TestLoader(unittest.TestCase):
    def test_valid_locations(self):

        """Testing known locations for longitude and latitude"""

        geolocator = get_geolocator()
        locations = {
            "Museum of Modern Art": {
                "latitude": 40.7618552,
                "longitude": -73.9782438,
                "type": "Museum"
            },
            "USS Alabama Battleship Memorial Park": {
                "latitude": 30.684373,
                "longitude": -88.015316,
                "type": "Park"
            },
        }
        for name, expect in locations.items():
            rec = fetch_location_data(geolocator, name)
            self.assertIsNotNone(rec, f'Should return a result')
            self.assertEqual(rec['location'], name)

            self.assertAlmostEqual(rec['latitude'], expect["latitude"], places=2)
            self.assertAlmostEqual(rec['longitude'], expect["longitude"], places=2)

            self.assertIn(expect["type"].lower(), (rec['type'] or '').lower())
            
        return None
    

    def test_invalid_location(self):
        """Test that invalid locations appear as rows with NaN values in the DataFrame."""

        geolocator = get_geolocator()
        result = fetch_location_data(geolocator, "asdfqwer1234")

        # Assert the result is a dictionary
        self.assertIsInstance(result, dict, "Result should be a dictionary.")

        # Assert the result contains expected NA values
        self.assertEqual(result["location"], "asdfqwer1234", "Location name should match the input.")
        self.assertIsNone(result["latitude"], "Latitude should be None for invalid locations.")
        self.assertIsNone(result["longitude"], "Longitude should be None for invalid locations.")
        self.assertIsNone(result["type"], "Type should be None for invalid locations.")

if __name__ == "__main__":
    unittest.main()
