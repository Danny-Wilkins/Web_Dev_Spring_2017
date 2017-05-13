import requests
import json
import operator
import numpy as np
from scipy import stats
from geopy.geocoders import Nominatim

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'
BEARER_TOKEN = "cwbsWBjL2SIw7I3_-4sD5dCo1Fxj3Te2wP4QKXsoVRBowf0UWRPtlKlq6eici0tE6ffVlIYN3oNZPoYH_6br4mfy0kwrhbMjZZrMuOqEOUkGTo4Qt7gG8oVZTiEWWXYx"

def authenticate():
	client_id = "XRYdDW2W0jN3S5ZDt6v1qA"
	client_secret = "WDNxkqLEzcWIWoAIW17q77BqeJYce9AgnrrZ9p3o05baXBpKPahRjOVfA6qHfkpw"
	print requests.post("https://api.yelp.com/oauth2/token", data = {"grant_type":"client_credentials", "client_id":"XRYdDW2W0jN3S5ZDt6v1qA", "client_secret":"WDNxkqLEzcWIWoAIW17q77BqeJYce9AgnrrZ9p3o05baXBpKPahRjOVfA6qHfkpw"}).content
	
	"""
	{"access_token": "cwbsWBjL2SIw7I3_-4sD5dCo1Fxj3Te2wP4QKXsoVRBowf0UWRPtlKlq6eici0tE6ffVlIYN3oNZPoYH_6br4mfy0kwrhbMjZZrMuOqEOUkGTo4Qt7gG8oVZTiEWWXYx", 
	"expires_in": 15551804, 
	"token_type": "Bearer"}
	"""

def getRestaurantsInArea(address, term="restaurant", radius=500, limit=20, open_now=False): #Radius in meters
	try:
		loc = geolocator(address)
	except:
		print "Location not found. Please try again."
		return getRestaurantsInArea(raw_input("Enter address: "))

	url = 'https://api.yelp.com/v3/businesses/search?term={}&latitude={}&longitude={}&radius={}&limit={}&open_now={}'.format(term, loc['lat'], loc['lng'], radius, limit, open_now)
	headers = {'Authorization':'Bearer {}'.format("cwbsWBjL2SIw7I3_-4sD5dCo1Fxj3Te2wP4QKXsoVRBowf0UWRPtlKlq6eici0tE6ffVlIYN3oNZPoYH_6br4mfy0kwrhbMjZZrMuOqEOUkGTo4Qt7gG8oVZTiEWWXYx")}

	response = requests.request('GET', url, headers=headers, params=None)

	return response.json()

def geolocator(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    print(location.address)

    #print location.latitude, location.longitude

    return {'lat':location.latitude, 'lng':location.longitude}

def value(item, slope, intercept):
	try:
		predicted = len(item['price']) * slope + intercept

		actual = float(item['rating'])

		deviation = round(actual - predicted, 3) * 100

		return deviation

	except:
		return 0

def grade(value):
	if 100 > value > 66:
		return 'A'
	elif 66 >= value > 33:
		return 'B'
	elif 33 >= value > -33:
		return 'C'
	elif -33 >= value > -66:
		return 'D'
	elif -66 >= value:
		return 'F'
	else:
		return 'A'

def main():

	js = getRestaurantsInArea(raw_input("Enter address: "))
	#print json.dumps(js['businesses'][0]['name'], indent=4, sort_keys=True)

	prices = []
	ratings = []

	for item in js['businesses']:
		try:
			prices.append(float(len(item['price'])))
			ratings.append(float(item['rating']))
		except:
			continue

	prices = np.array(prices)
	ratings = np.array(ratings)

	try:
		slope, intercept, r_value, p_value, std_err = stats.linregress(prices, ratings)
	except:
		print "No restaurants found nearby. Please try again."
		return getRestaurantsInArea(raw_input("Enter address: "))

	values = {}

	for item in js['businesses']:
		try:
			#print item['name'], value(item, slope, intercept)
			v = value(item, slope, intercept)

			values[item['name']] = (round(v, 3), grade(v))

		except: 
			continue

	values = sorted(values.items(), key=operator.itemgetter(1), reverse=True)

	index = 1

	for i in values:
		print index
		print i[0], '\n', i[1][0], '\n', i[1][1]
		print '*' * 20
		index+=1
	
if __name__ == '__main__':
	main()