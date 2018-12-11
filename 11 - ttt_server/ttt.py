import sys
import json
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

port_number = int(sys.argv[1])
dictionaryOfGames = dict()

class Game:
	def __init__(self, name):
		self.name = name
		self.nextPlayer = 1
		self.board = [[0, 0, 0],\
					  [0, 0, 0],\
					  [0, 0, 0]]
		self.winner = None

	def getNextPlayer(self):
		if(self.nextPlayer == 1):
			return 2
		else:
			return 1

	def mark(self,x, y):
		self.board[x][y] = self.nextPlayer
		self.whoWon()
		self.nextPlayer = self.getNextPlayer()
		return

	def whoWon(self):
		if self.winner != None:
			return

		if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
			self.winner = self.board[0][0]
			return
		if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
			self.winner = self.board[0][2]
			return

		for i in range(3):
			if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
				self.winner = self.board[i][0]
				return
				
		for j in range(3):
			if self.board[0][j] == self.board[1][j] == self.board[2][j] != 0:
				self.winner = self.board[0][j]
				return
		
		hasEmptySpot = False
		
		for smallList in self.board:
			for value in smallList:
				if(value == 0):
					hasEmptySpot = True
					
		if(hasEmptySpot == False):
			self.winner = 0

def StartGame(name):
	gameId = len(dictionaryOfGames) + 1
	dictionaryOfGames[gameId] = Game(name)
	return gameId

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	pass
	

class myHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		code, response = self.get_response()
		self.send_response(code)
		self.send_header("Content-type", "application/json")
		self.send_header( "Connection", "close")
		self.end_headers()
		self.wfile.write(response)
		return
			
	def get_response(self):
		splittedRequest = self.path[1:].split('?')
		
		if splittedRequest[0] not in ("start", "status", "play"):
			return HTTPStatus.BAD_REQUEST, bytes(json.dumps({}), "utf-8")
		
		if splittedRequest[0] == "start":
			name = ""
			
			if(len(splittedRequest) == 1):
				name = ""
			else:
				arguments = splittedRequest[1].split('&')
				
				pattern = re.compile(r"name=(.*)")
				for argument in arguments:
					match = pattern.match(argument)
					if match != None:
						name = match.group(1)
						break
			
			gameId = StartGame(name)
			return HTTPStatus.OK, bytes(json.dumps({"id": gameId}, indent=1), "utf-8")

		if len(splittedRequest) != 2:
			return HTTPStatus.BAD_REQUEST, bytes(json.dumps({}), "utf-8")
		
		if splittedRequest[0] == "status":
			arguments = splittedRequest[1].split('&')
			
			gameId = -1
			pattern = re.compile(r"game=(\d)")
			for argument in arguments:
				match = pattern.match(argument)
				if match != None:
					gameId = int(match.group(1))
					break
			
			if(gameId not in dictionaryOfGames):
				return HTTPStatus.BAD_REQUEST, bytes(json.dumps({}), "utf-8")
				
			game = dictionaryOfGames[gameId]
			result = {}

			if game.winner is not None:
				result["winner"] = game.winner
			else:
				result["board"] = game.board
				result["next"] = game.nextPlayer
				
			return HTTPStatus.OK, bytes(json.dumps(result, indent = 4), "utf-8")

		if splittedRequest[0] == "play":
			arguments = splittedRequest[1].split('&')
			
			gameId = -1
			player = -1
			x = -1
			y = -1
			
			patternGame = re.compile(r"game=(\d)")
			patternPlayer = re.compile(r"player=(\d)")
			patternX = re.compile(r"x=(\d)")
			patternY = re.compile(r"y=(\d)")
			
			for argument in arguments:
				matchGame = patternGame.match(argument)
				if matchGame != None:
					gameId = int(matchGame.group(1))
				
				matchPlayer = patternPlayer.match(argument)
				if matchPlayer != None:
					player = int(matchPlayer.group(1))
				
				matchX = patternX.match(argument)
				if matchX != None:
					x = int(matchX.group(1))
					
				matchY = patternY.match(argument)
				if matchY != None:
					y = int(matchY.group(1))
			
			if(gameId == -1 or player == -1 or x == -1 or y == -1):
				return HTTPStatus.BAD_REQUEST, bytes(json.dumps({}), "utf-8")
			
			if(gameId not in dictionaryOfGames):
				return HTTPStatus.BAD_REQUEST, bytes(json.dumps({}), "utf-8")
				
			game = dictionaryOfGames[gameId]
					
			if game.winner is not None:
				return HTTPStatus.OK, bytes(json.dumps({"status": "bad", "message": "Game has ended"}, indent=1), "utf-8")
				
			if player != game.nextPlayer:
				return HTTPStatus.OK, bytes(json.dumps({"status": "bad", "message": "It is not your turn"}, indent=1), "utf-8")
				
			if x < 0 or x > 2:
				return HTTPStatus.OK, bytes(json.dumps({"status": "bad", "message": "Wrong coordinates of x"}, indent=1),"utf-8")
			
			if y < 0 or y > 2:
				return HTTPStatus.OK, bytes(json.dumps({"status": "bad", "message": "Wrong coordinates of y"}, indent=1),"utf-8")
			
			if game.board[x][y] != 0:
				return HTTPStatus.OK, bytes(json.dumps({"status": "bad", "message": "This field is already taken"}, indent=1), "utf-8")
			
			game.mark(x,y)
			return HTTPStatus.OK, bytes(json.dumps({"status": "ok"}, indent=1), "utf-8")

server = ThreadedHTTPServer(('', port_number), myHandler)			
server.serve_forever()
