from flask import Flask
from flask import jsonify
from flask import request
import requests
import json

app = Flask(__name__)

if __name__ == '__main__':
    app.run()

def testReqs():
	print("i am here 0")

	origin = "Boston+MA"
	destination = "Shrewsbury+MA"
	key = "123123"
	#make the call to google maps
	
	uri = "https://maps.googleapis.com/maps/api/directions/json?"
	ret = requests.get(uri+"origin="+origin+"&destination="+destination+"&key="+key)
	print(ret.content)
	#return ret
testReqs()

@app.route("/")
def hello():
	return "Hello, Worldo!"
	
@app.route("/hello")
def hello2():
	print("helloing")
	return jsonify({'hello':'world'})
	
@app.route("/directions")
def directions():
	print("i am here 1")
	
	origin = request.args.get('start')
	destination = request.args.get('end')
	key = "123123"
	#make the call to google maps
	uri = "https://maps.googleapis.com/maps/api/directions/json?"
	ret = requests.get(uri+"origin="+origin+"&destination="+destination+"&key="+key)
	print(ret.content)
	return ret.content
	
@app.route("/directionsTest")
def directionsTest():
	print("i am here 2")
	
	origin = "Boston+MA"
	destination = "Shrewsbury+MA"
	key = "123123"
	#make the call to google maps
	uri = "https://maps.googleapis.com/maps/api/directions/json?"
	ret = requests.get(uri+"origin="+origin+"&destination="+destination+"&key="+key)
	print(ret.content)
	return ret.content
	
@app.route("/newJourney")
def newJourney():
	print("Creating New Journey")
	origin = request.args.get('start')
	destination = request.args.get('end')
	name = request.args.get('name')
	key = "123123"
	#make the call to google maps
	uri = "https://maps.googleapis.com/maps/api/directions/json?"
	ret = requests.get(uri+"origin="+origin+"&destination="+destination+"&key="+key)
	print(ret.content)
	directions = (ret.content).decode('utf-8').replace("\"","'")
	
	newJourney = {}
	newJourney["name"] = name
	newJourney["start"] = origin
	newJourney["end"] = destination
	newJourney["directions"] = directions
	return newJourney
