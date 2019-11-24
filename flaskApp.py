from flask import Flask
from flask import jsonify
from flask import request
import requests
import json
#import config #to access an apiKey, use the name of the variable from config.py, i.e. config.apiKey1
import os

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
	
	#make the call to google maps
	uri = "https://maps.googleapis.com/maps/api/directions/json?"
	ret = requests.get(uri+"origin="+origin+"&destination="+destination+"&key="+key)
	print(ret.content)
	return ret.content
	
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
def getWaypoint():
	print("Getting Waypoints...")
	origin = request.args.get('start')
	destination = request.args.get('end')
	interests = request.args.get('interests') #list of interest tags
	budgetRemaining = requests.args.get('budgetRemaining') #budget in usd
	
	
	key = "123123"
	#make the call to google maps
	uri = "https://maps.googleapis.com/maps/api/directions/json?"
	ret = requests.get(uri+"origin="+origin+"&destination="+destination+"&key="+key)
	print(ret.content)
	waypoints = []#(ret.content).decode('utf-8').replace("\"","'")
	
	
	newWaypoint = {}
	newJourney["waypoints"] = waypoints
	
	
	
	return newWaypoint
	
	
	
	
	
#HELPER FUNCTIONS
def mapApiForAverageDriveTime(start,end):
	
	#make the call to google maps to return the driving time between 2 points
	uri = "https://maps.googleapis.com/maps/api/distancematrix/json?"
	ret = requests.get(uri+"origins="+start+"&destinations="+end+"&key="+key)
	
	#retContent = ((ret.content).decode('utf-8').replace("\"","'")) NOT USED
	retContent = ret.json()
	return retContent["rows"][0]["elements"][0]["duration"]["value"]
	
	
















	
	