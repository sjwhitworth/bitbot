import pika
import random
import time
import json
from websocket import create_connection

class Ticker():
	def __init__(self, publisher, qname):
		self.publisher = publisher
		self.qname = qname

	def connect_to_mtgox_socket(self):
		self.ws = create_connection("wss://websocket.mtgox.com:443/mtgox?Currency=USD,EUR,JPY,GBP")

	def monitor(self):
		self.connect_to_mtgox_socket()
		while True:
			data = self.ws.recv()
			json_data = json.loads(data)
			print json_data
			self.publisher.publish(json.dumps(json_data), routing_key=json_data['channel_name'])