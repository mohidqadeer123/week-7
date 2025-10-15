'''
Script to load geographical data into a pandas DataFrame, and save it as a CSV file.
'''

from geopy.geocoders import Nominatim
import pandas as pd


def get_geolocator(agent='h501-student'):
    """
    Initiate a Nominatim geolocator instance given an `agent`.
    """
    return Nominatim(user_agent=agent)

def fetch_location_data(geolocator, loc):
    """Fetch latitude, longitude, and type for a given location string.
    """
    try:
        location = geolocator.geocode(loc)

    except Exception:
        return None

    if not location:
        return None
    
    if location is None:
        return None
    
    return {
        "location": loc,
        "latitude": location.latitude,
        "longitude": location.longitude,
        "type": getattr(location, 'raw', {}).get('type')
    }

def build_geo_dataframe(locations):

    """Build a pandas DataFrame from a list of location names.
    """
    geolocator = get_geolocator()
    rows = []
    
    for name in locations:
        rec = fetch_location_data(geolocator, name)
       
        if rec is None:
            rows.append({
                "location": name,
                "latitude": None,
                "longitude": None,
                "type": None
            })
        else:
            rows.append(rec)

    return pd.DataFrame.from_records(rows, columns=["location", "latitude", "longitude", "type"])



if __name__ == "__main__":
    geo = get_geolocator()

    locations = ["Museum of Modern Art", "iuyt8765(*&)", "Alaska", "Franklin's Barbecue", "Burj Khalifa"]

    df = build_geo_dataframe(locations)

    df.to_csv("./geo_data.csv")
