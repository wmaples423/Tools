# # get two locations: origin and destination
origin_add = input("Enter street address: ").upper()
origin_city = input("Enter city: ").upper()
origin_state = input("Enter state: ").upper()
origin_zip = input("Enter zip code: ")
origin = origin_add + " " + origin_city + " " + origin_state + " " + origin_zip
print(origin)

destination_add = input("Enter street address: ").upper()
destination_city = input("Enter city: ").upper()
destination_state = input("Enter state: ").upper()
destination_zip = input("Enter zip code: ")
destination = destination_add + " " + destination_city + " " + destination_state + " " + destination_zip
print(destination)
# determine optimal route
import requests

def get_geocode_google(address):
    params = {
        'key': 'YOUR_GOOGLE_MAPS_API_KEY',
        'address': address
    }
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
    data = response.json()
    if data['results']:
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        return None, None

origin_add = input("Enter street address: ").upper()
origin_city = input("Enter city: ").upper()
origin_state = input("Enter state: ").upper()
origin_zip = input("Enter zip code: ")
origin = origin_add + " " + origin_city + " " + origin_state + " " + origin_zip

lat, lng = get_geocode_google(origin)
print(f'Latitude: {lat}, Longitude: {lng}')

# calculate distance between them
# pull gas price from google maps
# calculate cost of trip

# import all locations from a table
# run calculations on all locations as origins and destinations to get all calculations