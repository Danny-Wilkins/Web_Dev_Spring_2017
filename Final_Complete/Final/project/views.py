from flask import render_template
from app import app, pages
import requests
import json
import operator
import os
import numpy as np
from scipy import stats
from geopy.geocoders import Nominatim

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search/<address>')

def search(address):
	geolocator = Nominatim()
	loc = geolocator.geocode(address).address

	js = getRestaurantsInArea(address)

	with open('static/data/json.txt', 'w') as json_file:
		json_file.write(json.dumps(js, indent=4, sort_keys=True))

	prices = []
	ratings = []

	#print('About to get to business')

	for item in js['businesses']:
		try:
			prices.append(float(len(item['price'])))
			ratings.append(float(item['rating']))
		except:
			continue

	prices = np.array(prices)
	ratings = np.array(ratings)

	#print('About to do some math')

	try:
		slope, intercept, r_value, p_value, std_err = stats.linregress(prices, ratings)
	except:
		#print "No restaurants found nearby. Please try again."
		return getRestaurantsInArea(address)

	values = {}



	for item in js['businesses']:
		try:
			#print item['name'], value(item, slope, intercept)
			v = value(item, slope, intercept)

			values[item['name']] = (rate(v), grade(v))

		except: 
			continue

	values = sorted(values.items(), key=operator.itemgetter(1), reverse=True)

	data = {}
	index = 0

	for i in values:
		#print(i)
		data[index] = (str(i[1][0]), str(i[1][1]))
		index += 1

	print(loc, '\n')

	page = ''
	new_page = 'templates/results.html'

	with open('templates/index.html', 'r') as index:
		for line in index:
			#print(line)
			if '</body>' in line: 
				continue
			elif '</html>' in line: 
				continue
			page += line

	html_data = '''<div class="container">
						<div class="row">
	            			<div class="col-sm-11">
	                		<h3>{}</h3>
	                		</div>
            			</div>
            		</div>\n'''.format(loc)

	for i in range(0, 20):
		try:
			name = json.dumps(js['businesses'][i]['name']).replace("\"", "")
			title = json.dumps(js['businesses'][i]['categories'][0]['title']).replace("\"", "")
			distance = json.dumps(js['businesses'][i]['distance']) #In meters
			miles = round(float(distance) * 0.000621371, 2) #In miles
			image_url = js['businesses'][i]['image_url']
			#image_url = image_url.replace("https://", "")
			phone = json.dumps(js['businesses'][i]['phone']).replace("\"", "")
			price = json.dumps(js['businesses'][i]['price']).replace("\"", "")
			rating = json.dumps(js['businesses'][i]['rating']).replace("\"", "") + '/5'
			reviews = json.dumps(js['businesses'][i]['review_count']).replace("\"", "")
			url = json.dumps(js['businesses'][i]['url']).replace("\"", "")
			add = json.dumps(js['businesses'][i]['location']['address1']).replace("\"", "")
			html_data += '''<div class="container">
			<a href="{}" target="_blank">
			<div class="jumbotron" id="result">
			<div class="block" style="background-image: url({}); background-size:cover;"></div>
	        <div class="row">
	            <div class="col-sm-8">
	                <h2>{}</h2>
	                <h4>{} miles</h4>
	                <h4>{}</h4>
	                <h4>{}</h4>
	            </div>
	            <div class="col-sm-2">
	                <h2>{}</h2>
	                <h4>{} reviews</h4>
	                <h2>{}</h2>
	            </div>
	            <div class="col-sm-1 col-sm-offset-1">
	                <h1>{}</h1>
	                <h3>{}</h3>
	            </div>
	        </div>
	        </div>
	    </div>\n
	    </a>'''.format(url, image_url, name, miles, add, phone, rating, reviews, price, data[i][1], data[i][0])
		except:
			continue

	with open(new_page, 'w') as new:
		new.write(page)
		new.write(html_data)
		new.write('</body>\n<html>')

	return render_template('results.html')

def geolocator(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    #print(location.address)

    #print location.latitude, location.longitude

    return {'lat':location.latitude, 'lng':location.longitude}

def getRestaurantsInArea(address="2 metrotech center", term="restaurant", radius=1000, limit=20, open_now=False): #Radius in meters
	try:
		loc = geolocator(address)
	except:
		#print "Location not found. Please try again."
		return getRestaurantsInArea(address)

	url = 'https://api.yelp.com/v3/businesses/search?term={}&latitude={}&longitude={}&radius={}&limit={}&open_now={}&sort=1'.format(term, loc['lat'], loc['lng'], radius, limit, open_now)
	headers = {'Authorization':'Bearer {}'.format("cwbsWBjL2SIw7I3_-4sD5dCo1Fxj3Te2wP4QKXsoVRBowf0UWRPtlKlq6eici0tE6ffVlIYN3oNZPoYH_6br4mfy0kwrhbMjZZrMuOqEOUkGTo4Qt7gG8oVZTiEWWXYx")}

	response = requests.request('GET', url, headers=headers, params=None)

	return response.json()

def value(item, slope, intercept):
	try:
		predicted = len(item['price']) * slope + intercept

		actual = float(item['rating'])

		deviation = round(actual - predicted, 3) * 100

		return deviation

	except:
		#print "Something went wrong. Please try again."
		return getRestaurantsInArea()

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

def rate(value):
	if 100 > value > 66:
		return 'Great!'
	elif 66 >= value > 33:
		return 'Good!'
	elif 33 >= value > -33:
		return 'Average!'
	elif -33 >= value > -66:
		return 'Bad!'
	elif -66 >= value:
		return 'Terrible!'
	else:
		return 'Great!'