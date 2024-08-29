import numpy as np
import os
import requests
from Secrets import get_secrets

# Access the API key
api_key = get_secrets()['API_KEY']
base_url = "https://maps.googleapis.com/maps/api/geocode/json"
R = 6371

class Point:
    cartesian = np.array([])
    polar = []
    postcode = []

    def __init__(self, cartesian, polar, postcode):
        self.cartesian = cartesian
        self.normal = (1/R)*self.cartesian
        self.polar = polar
        self.postcode = postcode

    @classmethod
    def fromPolar(cls, polar):
        lat = np.radians(polar[0])
        lng = np.radians(polar[1])

        x = R * np.cos(lat)*np.cos(lng)
        y = R * np.cos(lat)*np.sin(lng)
        z = R * np.sin(lat)

        endpoint = f"{base_url}?latlng={polar[0]}, {polar[1]}&key={api_key}"
        r = requests.get(endpoint)
        
        if r.status_code==200:
            json_data = r.json()
            if "results" in json_data and len(json_data["results"]) > 0:
                postcode = json_data['results'][0]['address_components']
            else:
                postcode = None
        else:
            postcode = None

        return cls(cartesian=np.array([x, y, z]), polar=polar, postcode=postcode)

    @classmethod
    def fromCartesian(cls, cartesian):
        lat = np.degrees(np.asin(cartesian[2] / R))
        lng = np.degrees(np.atan2(cartesian[1], cartesian[0]))

        endpoint = f"{base_url}?latlng={lat}, {lng}&key={api_key}"
        r = requests.get(endpoint)
        if r.status_code==200:
            json_data = r.json()
            if "results" in json_data and len(json_data["results"]) > 0:
                postcode = json_data['results'][0]['address_components']
            else:
                postcode = None
        else:
            postcode = None

        return cls(cartesian=np.array(cartesian), polar=[lat, lng], postcode=postcode)

    @classmethod
    def fromAddress(cls, postcode):

        endpoint = f"{base_url}?address={postcode}&key={api_key}"

        r = requests.get(endpoint)
        if r.status_code == 200:
            json_data = r.json()
            if "results" in json_data and len(json_data["results"]) > 0:
                postcode=json_data['results'][0]['address_components']
                lat = json_data['results'][0]['geometry']['location']['lat']
                lng = json_data['results'][0]['geometry']['location']['lng']
                polar = [lat, lng]

                x = R * np.cos(np.radians(lat)) * np.cos(np.radians(lng))
                y = R * np.cos(np.radians(lat)) * np.sin(np.radians(lng))
                z = R * np.sin(np.radians(lat))

                return cls(cartesian=np.array([x, y, z]), polar=polar, postcode=postcode)
            else:
                return False
        else:
            return False
        
    def to_dict(self):
        return {
            "cartesian": {
                "x": self.cartesian[0], 
                "y": self.cartesian[1],
                "z": self.cartesian[2]
            },
            "polar": {
                "latitude": self.polar[0],
                "longitude": self.polar[1]
            },
            "address": self.postcode
        }
    
    @staticmethod
    def from_dict(data):
        return Point(
            np.array([data['cartesian']['x'], data['cartesian']['y'], data['cartesian']['z']]),
            [data['polar']['latitude'], data['polar']['longitude']],
            data['address']
                     )

    def __str__(self):
        return f"({self.polar[0]:.6f}, {self.polar[1]:.6f})"

    def verbose(self):
        # Format Cartesian coordinates
        cartesian_str = (f"Cartesian Coordinates: x={self.cartesian[0]:.2f}, "
                        f"y={self.cartesian[1]:.2f}, z={self.cartesian[2]:.2f}\n")
        
        # Format Polar coordinates
        polar_str = (f"Polar Coordinates: latitude={self.polar[0]:.2f}°, "
                    f"longitude={self.polar[1]:.2f}°\n")
        
        # Check if postcode is None and format accordingly
        if self.postcode is not None and len(self.postcode) > 0:
            postcode_str = f"Postcode: {self.postcode[0]['long_name']}"
        else:
            postcode_str = "Postcode: Not available"
        
        # Combine all parts into the final string
        return cartesian_str + polar_str + postcode_str
