import sys
import socket
import urllib.request
import json
from urllib.error import HTTPError
from http.server import BaseHTTPRequestHandler, HTTPServer

port_number = int(sys.argv[1])
upstream = sys.argv[2]
	
class myHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		responseForClient = {}
		request = urllib.request.Request(url = upstream, headers = dict(self.headers))
		
		try:
			response = urllib.request.urlopen(request, timeout=1)
		except HTTPError as error:
			responseForClient['code'] = error.code
			responseForClient['headers'] = dict(error.headers.items())
		except socket.timeout:
			responseForClient['code'] = 'timeout'
		else:	
			responseForClient['code'] = response.code
			responseForClient['headers'] = dict(response.headers.items())
			resp = bytes.decode(response.read(), 'utf-8')
			try:
				responseForClient['json'] = json.loads(resp)
			except ValueError:
				responseForClient['content'] = resp
			
		self.send_response(200, 'OK')
		self.send_header('Connection', 'close')
		self.end_headers()
		self.wfile.write(bytes(json.dumps(responseForClient), 'utf-8'))
		return

	def do_POST(self):
		responseForClient = {}
		if 'Content-Length' not in self.headers:
			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			responseForClient["code"] = "invalid json"
			self.wfile.write(bytes(json.dumps(responseForClient), 'utf-8'))
			return
		else:
			content = self.rfile.read(int(self.headers['Content-Length']))
		

		jsonContent = None
		try:
			jsonContent = json.loads(content)
		except ValueError:
			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			responseForClient["code"] = "invalid json"
			self.wfile.write(bytes(json.dumps(responseForClient), 'utf-8'))
			return
		
		if 'type' not in jsonContent.keys():
			jsonContent['type'] = 'GET'
		if jsonContent['type'] == 'GET':
			jsonContent['content'] = None
		if 'timeout' not in jsonContent.keys():
			jsonContent['timeout'] = 1
		if 'headers' not in jsonContent.keys():
			jsonContent['headers'] = None
			

		
		if 'url' not in jsonContent.keys() or (jsonContent['type'] == 'POST' and 'content' not in jsonContent.keys()):
			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			responseForClient["code"] = "invalid json"
			self.wfile.write(bytes(json.dumps(responseForClient), 'utf-8'))
			return
		
		data = None
		if(jsonContent['content'] != None):
			data = str(jsonContent['content']).encode('UTF-8')
			request = urllib.request.Request(url = jsonContent['url'], data = data, headers = jsonContent['headers'], method = jsonContent['type'])
		else:
			request = urllib.request.Request(url = jsonContent['url'], headers = jsonContent['headers'], method = jsonContent['type'])
		
		try:
			response = urllib.request.urlopen(request, timeout=jsonContent['timeout'])
		except HTTPError as error:
			responseForClient['code'] = error.code
			responseForClient['headers'] = dict(error.headers.items())
		except socket.timeout:
			responseForClient['code'] = 'timeout'
		else:	
			responseForClient['code'] = response.code
			responseForClient['headers'] = dict(response.headers.items())
			resp = bytes.decode(response.read(), 'utf-8')
			try:
				responseForClient['json'] = json.loads(resp)
			except ValueError:
				responseForClient['content'] = resp

		self.send_response(200, 'OK')
		self.send_header('Connection', 'close')
		self.end_headers()
		self.wfile.write(bytes(json.dumps(responseForClient), 'utf-8'))
		return
		
server = HTTPServer(('', port_number), myHandler)
server.serve_forever()
