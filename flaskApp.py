from flask import Flask
from flask import jsonify
from flask import request
import math
import random
import requests
import json
import os
from decoder_gistfile1 import decode

app = Flask(__name__)
key = os.getenv("apiKey")

if __name__ == '__main__':
    app.run()

def testReqs(): #never invoked
	print("Running function restReqs")
	origin = "Boston+MA"
	destination = "Shrewsbury+MA"
	#make the call to google maps
	uri = "https://maps.googleapis.com/maps/api/directions/json?"
	ret = requests.get(uri+"origin="+origin+"&destination="+destination+"&key="+key)
	print(ret.content)


@app.route("/")
def hello():
	print("Running function hello")
	return "Hello, Worldo!"
	
@app.route("/hello")
def hello2():
	print("Running function hello2")
	print("helloing")
	return jsonify({'hello':'world'})
	
@app.route("/directions")
def directions():
	print("Running function directions")
	
	origin = request.args.get('start')
	destination = request.args.get('end')
	
	return directions2(origin,destination)
	
def directions2(origin,destination):#directions but as a function instead of an api endpoint
	print("Running function directions2")

	#make the call to google maps
	uri = "https://maps.googleapis.com/maps/api/directions/json?"
	ret = requests.get(uri+"origin="+origin+"&destination="+destination+"&key="+key)
	#print(ret.content)
	return ret.json()
	
@app.route("/directionsTest")
def directionsTest():
	print("Running function directionsTest")
	
	origin = "Boston+MA"
	destination = "Shrewsbury+MA"
	
	#make the call to google maps
	uri = "https://maps.googleapis.com/maps/api/directions/json?"
	ret = requests.get(uri+"origin="+origin+"&destination="+destination+"&key="+key)
	print(ret.content)
	return ret.content
	
@app.route("/newJourney")
def newJourney():
	print("Creating New Journey")
	start = request.args.get('start') #geolocation OR textual address representation of the point A
	end = request.args.get('end') #geolocation OR textual address representation of the point M
	type = request.args.get('type') #string representing journey type, either aej, rtj, or owj
	time = int(request.args.get('time')) #time in seconds of how long the user wants to be travelling (on the road! not at waypoints)
	budget = int(request.args.get('budget')) #USD value of how much money the user plans to spend
	name = request.args.get('name') #name of new Journey
	
	averageDriveTime = mapApiForAverageDriveTime(start,end)
	
	if type != "owj":
		averageDriveTime = averageDriveTime + mapApiForAverageDriveTime(end,start)
	
	timeRemaining = time - averageDriveTime
	
	budgetRemaining = budget
	
	
	newJourney = {}
	waypoints = []
	
	waypoints = waypoints + [start,end]
	if type != "owj":
		waypoint = waypoints + [start]
	
	
	newJourney["name"] = name
	newJourney["start"] = start
	newJourney["end"] = end
	newJourney["budget"] = budget
	newJourney["budgetRemaining"] = budgetRemaining
	newJourney["time"] = time
	newJourney["timeRemaining"] = timeRemaining
	#newJourney["directions"] = directions
	newJourney["waypoints"] = waypoints
	return newJourney

@app.route("/getWaypoints")
def getWaypoints():
	print("Getting Waypoints...")
	origin = request.args.get('start')
	destination = request.args.get('end')
	interests = (request.args.get('interests'))[1:-1].split(",") #list of interest tags
	spacing = request.args.get('spacing') #either 'even' or 'random' optional parameter
	#budgetRemaining = requests.args.get('budgetRemaining') #budget in usd
	numOfStops = int(request.args.get('num'))
	
	numOfInterests = len(interests)
	if spacing == None or spacing.equals("random"):
		midpoints = directionsMidpointsFinder(origin,destination,numOfStops)
	else: #even spacing is the default parameter
		midpoints = midpointsFinder(origin,destination,numOfStops)
	
	random.shuffle(interests)

	#return midpoints
	#make the call to google maps
	#uri = "https://maps.googleapis.com/maps/api/directions/json?"
	#ret = requests.get(uri+"origin="+origin+"&destination="+destination+"&key="+key)
	#print(ret.content)
	#[]#(ret.content).decode('utf-8').replace("\"","'")
	waypoints = []
	for x in range(len(midpoints)):
		waypoints += [getWaypoint(midpoints[x],interests[x%numOfInterests])]
	
	newWaypoints = {}
	newWaypoints["waypoints"] = waypoints
	
	return newWaypoints
	
	
#HELPER FUNCTIONS
def mapApiForAverageDriveTime(start,end):
	#make the call to google maps to return the driving time between 2 points
	uri = "https://maps.googleapis.com/maps/api/distancematrix/json?"
	ret = requests.get(uri+"origins="+start+"&destinations="+end+"&key="+key)
	
	#retContent = ((ret.content).decode('utf-8').replace("\"","'")) NOT USED
	retContent = ret.json()
	return retContent["rows"][0]["elements"][0]["duration"]["value"]
	
def getLatLong(point):
	#make the call to google maps to return the location or a point
	uri = "https://maps.googleapis.com/maps/api/geocode/json?"
	ret = requests.get(uri+"address="+point+"&key="+key)
	
	#retContent = ((ret.content).decode('utf-8').replace("\"","'")) NOT USED
	retContent = ret.json()
	#print(retContent)
	#print([retContent["results"][0]["geometry"]["location"]["lng"],retContent["results"][0]["geometry"]["location"]["lat"]])
	return [retContent["results"][0]["geometry"]["location"]["lng"],retContent["results"][0]["geometry"]["location"]["lat"]]


def midpointsFinder(start,end,num): #TODO, use OVERVIEWPOLYLINE and decoder from directions/road and geometry api to be closer to reasonable path traffic wise!
	midpoints = []
	
	#this is to prevent accidental waste of all api keys!
	num = min(num, 4)
	
	location1 = getLatLong(start)
	location2 = getLatLong(end)

	m = (location2[1] - location1[1])/(location2[0] - location1[0])
	
	lineFunc = lambda x : m*(x-location1[0]) + location1[1]

	#print( "math.sqrt(("+str(location1[0])+" - "+str(location2[0])+") + ("+str(location1[1])+" - "+str(location2[1])+"))")
	dist = math.sqrt((location1[0] - location2[0])**2 + (location1[1] - location2[1])**2)
	
	signModifier = 1
	if (location1[0]>location2[0]):
		signModifier = -1
	
	eachDist = (signModifier)*(dist / (num+1))
	
	currentDist = 0
	#print("("+str(location1[0])+","+str(location1[1])+")")
	#print("("+str(location2[0])+","+str(location2[1])+")")
	for x in range(num):
		
		currentDist = currentDist + eachDist
		nowX = location1[0]+currentDist
		midpoints += [(nowX,lineFunc(nowX))]
		#print((nowX,lineFunc(nowX)))
		#print(midpoints)
	
	return midpoints
	
def randpointsFinder(start,end,num): #can be used to find random points, with no guarantee of reasonable ordering! TODO make this reorder intelligently
	midpoints = []
	
	#this is to prevent accidental waste of all api keys!
	num = min(num, 4)
	
	location1 = getLatLong(start)
	location2 = getLatLong(end)

	m = (location2[1] - location1[1])/(location2[0] - location1[0])
	
	lineFunc = lambda x : m*(x-location1[0]) + location1[1]

	#print( "math.sqrt(("+str(location1[0])+" - "+str(location2[0])+") + ("+str(location1[1])+" - "+str(location2[1])+"))")
	dist = math.sqrt((location1[0] - location2[0])**2 + (location1[1] - location2[1])**2)
	
	signModifier = 1
	if (location1[0]>location2[0]):
		signModifier = -1
	
	
	currentDist = 0
	#print("("+str(location1[0])+","+str(location1[1])+")")
	#print("("+str(location2[0])+","+str(location2[1])+")")
	for x in range(num):
		
		currentDist = (signModifier)*math.uniform(0,dist)
		nowX = location1[0]+currentDist
		midpoints += [(nowX,lineFunc(nowX))]
		#print((nowX,lineFunc(nowX)))
		#print(midpoints)
	
	return midpoints


def directionsMidpointsFinder(start,end,num): #uses signed0's decoder function
	midpoints = []
	
	#this is to prevent accidental waste of all api keys!
	num = min(num, 4)
	
	encodedVal = directions2(start,end)

	#print(encodedVal)
	polylinePoints = decode(encodedVal["routes"][0]["overview_polyline"]["points"])

	#print("("+str(location1[0])+","+str(location1[1])+")")
	#print("("+str(location2[0])+","+str(location2[1])+")")
	
	totalNumOfPoints = len(polylinePoints)
	
	randPoints = []
	
	for x in range(num):
		randPoints += [random.randint(0,totalNumOfPoints)]
	
	randPoints.sort()
	
	for x in randPoints:
		midpoints += [(polylinePoints[x])]
		#print((nowX,lineFunc(nowX)))
		#print(midpoints)
	print("Midpoints = ", midpoints)
	
	return midpoints
	
def getWaypoint(coordinates,interest):
	#make the call to google maps to return the nearest loction with that interest
	coordinatesParam = (str(coordinates[1])+","+str(coordinates[0]))
	print(coordinatesParam)
	uri = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
	ret = requests.get(uri+"location="+coordinatesParam+"&radius=15000"+"&keyword="+interest+"&key="+key)
	print("https://maps.googleapis.com/maps/api/place/nearbysearch/json?"+"location="+coordinatesParam+"&radius=15000"+"&keyword="+interest+"&key="+key)
	#retContent = ((ret.content).decode('utf-8').replace("\"","'")) NOT USED
	retContent = ret.json()
	#print(retContent)
	#print([retContent["results"][0]["geometry"]["location"]["lng"],retContent["results"][0]["geometry"]["location"]["lat"]])
	print(retContent)
	return retContent["results"][0]["name"]














	
	