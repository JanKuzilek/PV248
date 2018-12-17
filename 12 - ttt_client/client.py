import sys
import http.client
import json
import re
import time

hostname = sys.argv[1]
port_number = int(sys.argv[2])

player = 0
currentGame = 0

connection = http.client.HTTPConnection(hostname, port_number)

def gameChoosing():
	userInput = input("")

	patternNew = re.compile(r"new(.*)")
	#not working
	patternJoin = re.compile(r"(\d)")
	
	if(patternNew.match(userInput)):
		global player
		global currentGame
		match = patternNew.match(userInput)
		name = match.group(1).strip()
		connection.request("GET", "/start?name={}".format(name))
		response = connection.getresponse()
		decodedResponse = response.read().decode('utf-8')
		jsonRepresentation = json.loads(decodedResponse)
		currentGame = jsonRepresentation["id"]
		player = 1
		UpdateClient()
	elif(patternJoin.match(userInput)):
		match = patternJoin.match(userInput)
		id = match.group(1)
		connection.request("GET", "/update?id={}".format(id))
		response = connection.getresponse()
		if(response.code == 200):
			currentGame = id
			player = 2
			UpdateClient()
		else:
			print("invalid input")
			gameChoosing()
	else:
		print("invalid input")
		gameChoosing()
		
def PrintMark(number):
	if(number == 0):
		return "_"
	elif(number == 1):
		return "x"
	elif(number == 2):
		return "o"

def UpdateClient():
	connection.request("GET", "/status?game={}".format(currentGame))
	response = connection.getresponse()
	decodedResponse = response.read().decode('utf-8')
	js = json.loads(decodedResponse)
	if("winner" in js):
		if(js["winner"] == 0):
			print("draw")
		elif(js["winner"] == player):
			print("you win")
		else:
			print("you lose")
		return
		
	print(str(PrintMark(js["board"][0][0])) + str(PrintMark(js["board"][0][1])) + str(PrintMark(js["board"][0][2])))
	print(str(PrintMark(js["board"][1][0])) + str(PrintMark(js["board"][1][1])) + str(PrintMark(js["board"][1][2])))
	print(str(PrintMark(js["board"][2][0])) + str(PrintMark(js["board"][2][1])) + str(PrintMark(js["board"][2][2])))
	
	if(js["next"] == player):
		inGame()
	else:
		print("waiting for the other player")
		currentResponse = js
		running= True
		while running:
			connection.request("GET", "/status?game={}".format(currentGame))
			response = connection.getresponse()
			decodedResponse = response.read().decode('utf-8')
			jsr = json.loads(decodedResponse)
			if(currentResponse.items() != jsr.items()):
				running = False				
			time.sleep(1)
		UpdateClient()
		
def inGame():
	inputString = ""
	if(player == 1):
		inputString = "your turn (x):"
	else:
		inputString = "your turn (o):"
	userInput = input(inputString)

	patternPlay = re.compile(r"(\d)\s(\d)")

	if(patternPlay.match(userInput)):
		match = patternPlay.match(userInput)
		x = match.group(1)
		y = match.group(2)
		
		connection.request("GET", "/play?game={}&player={}&x={}&y={}".format(currentGame,player,x,y))
		response = connection.getresponse()
		if(response.status != 200):
			print("invalid input")
			inGame()
		decodedResponse = response.read().decode('utf-8')
		js = json.loads(decodedResponse)
		if("message" in js):
			print(js["message"])
			inGame()
		else:
			UpdateClient()
	else:
		print("invalid input")
		inGame()
	
connection.request("GET", "/list")
response = connection.getresponse()
decodedResponse = response.read().decode('utf-8')
listOfDictionaries = json.loads(decodedResponse)

if(len(listOfDictionaries) == 0):
	print("There are no available games, please create a new one")
else:
	for dict in listOfDictionaries:
		print(str(dict["id"]) + " " + str(dict["name"]))

gameChoosing()
inGame()
					
connection.close()