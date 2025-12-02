
'''
Script to load geographical data into a pandas DataFrame, and save it as a CSV file.
'''

from geopy.geocoders import Nominatim
import pandas as pd


def get_geolocator(agent='h501-student'):
    """
    Initiate a Nominatim geolocator instance given an `agent`.

    Parameters
    ----------
    agent : str, optional
        Agent name for Nominatim, by default 'h501-student'
    """
    return Nominatim(user_agent=agent)

def fetch_location_data(geolocator, loc):
    """
    Fetch location data (latitude, longitude, type) for a given location.
    """
    try:
        location = geolocator.geocode(loc)
        if location is None:
            return {
                "location": loc,
                "latitude": None,
                "longitude": None,
                "type": None
            }

        return {
            "location": loc,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "type": location.raw.get("type", "unknown")
        }
    except Exception:
        return {
            "location": loc,
            "latitude": None,
            "longitude": None,
            "type": None
        }
    
def build_geo_dataframe(geolocator, locations):
    geo_data = [fetch_location_data(geolocator, loc) for loc in locations]
    
    return pd.DataFrame(geo_data)


if __name__ == "__main__":
    geo = get_geolocator()

    locations = ["Museum of Modern Art", "iuyt8765(*&)", "Alaska", "Franklin's Barbecue", "Burj Khalifa"]

    # inserting a try/except to debug and find an error 
    try:
        df = build_geo_dataframe(geo, locations)
        df.to_csv('./geo_data.csv', index=False)
        print('Geographical data saved to geo_data.csv')
    
    # printing the error message if the try code fails
    except Exception as e:
        print(f'An error occurred: {e}')
