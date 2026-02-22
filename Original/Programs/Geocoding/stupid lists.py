import gmaps
import requests
import json
from gmaps import Geocoding

with open('API-KEY.txt') as f:
    Key = f.readline()
    f.close()


def extract_lat_long_via_address(address_or_zipcode):
    lat, lng = None, None
    api_key = Key
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
    r = requests.get(endpoint)
    json_data = json.loads(r.text)
    return json_data

def extract_address_via_lat_long(lat, lng):
    api_key = Key
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?latlng={lat}, {lng}&key={api_key}"
    r = requests.get(endpoint)
    json_data = json.loads(r.text)
    return json_data['status']

print(extract_address_via_lat_long(52.3534224, -1.7820746))
