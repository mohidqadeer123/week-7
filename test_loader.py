import unittest
import pandas as pd
from loader import *

class TestLoader(unittest.TestCase):
    def test_valid_locations(self):

        """Testing known locations for longitude and latitude"""

        geolocator = get_geolocator()
        locations = ["Museum of Modern Art", "USS Alabama Battleship Memorial Park"]
        df = build_geo_dataframe(geolocator, locations)

        # Expected results (approximate)
        expected = {"Museum of Modern Art": (40.7618552, -73.9782438, "museum"), "USS Alabama Battleship Memorial Park": (30.684373, -88.015316, "park")}


        for _, row in df.iterrows():
            lat, lon, typ = expected[row["location"]]
            self.assertAlmostEqual(row["latitude"], lat, places=2)
            self.assertAlmostEqual(row["longitude"], lon, places=2)
            self.assertIn(typ.lower(), row["type"].lower())

        return None

    def test_invalid_location(self):
         """Test that invalid locations appear as rows with NaN values in the DataFrame."""

         geolocator = get_geolocator()
         invalid_locations = ["asdfqwer1234", "#####", "1234567890"]
         df = build_geo_dataframe(geolocator, invalid_locations)
         
         # Ensure DataFrame has the same number of rows as input locations
         self.assertEqual(len(df), len(invalid_locations))
         
         # Ensure expected columns exist
         expected_columns = {"location", "latitude", "longitude", "type"}
         self.assertTrue(expected_columns.issubset(df.columns))

        # --- Value checks for each row ---
        for idx, row in df.iterrows():

        # The location name should be preserved
        self.assertIn(row["location"], invalid_locations)

        # Latitude, longitude, and type should be missing (NaN)
        self.assertTrue(pd.isna(row["latitude"]), f"Latitude should be NaN for {row['location']}")
        self.assertTrue(pd.isna(row["longitude"]), f"Longitude should be NaN for {row['location']}")
        self.assertTrue(pd.isna(row["type"]), f"Type should be NaN for {row['location']}")

if __name__ == "__main__":
    unittest.main()
