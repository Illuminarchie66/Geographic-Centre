import gmaps
from gmaps import Geocoding

with open('API-KEY.txt') as f:
    Key = f.readline()
    f.close()

api = Geocoding(api_key = Key)
result = api.geocode("B901QJ", None, None, None, None, None)

result2 = api.reverse(30, 30, None, None, None, None)

#result2 = api.reverse(0, 0, None, None, None, None, None)
#api.reverse

lat = result[0]['geometry']['location']['lat']
lng = result[0]['geometry']['location']['lng']
#print(lat, lng)
print(result)

ZIPCode = result2[0]['address_components'][7]['long_name']
print(ZIPCode)
