import pika
import random
import time
import json
from websocket import create_connection

class Ticker():
	def __init__(self, publisher, qname):
		self.publisher = publisher
		self.stocks = ["MSFT", "AAPL", "YHOO", "LLOY"]
		self.last_quote = {}
		self.qname = qname

	def connect_to_mtgox_socket(self):
		self.ws = create_connection("wss://websocket.mtgox.com:443/mtgox?Currency=GBP")

	def get_quote(self):
		#Replace this logic with processing a quote from the MTGOX api
		stock = random.choice(self.stocks)
		if stock in self.last_quote:
			previous_quote = self.last_quote[stock]
			quote = random.uniform(0.99*previous_quote, 1.1*previous_quote)
		else:
			quote = random.uniform(30,250)
			self.last_quote[stock] = quote
		current_time = int(time.time())
		return {"stock": stock, "quote": quote, "current_time": current_time}

	def monitor(self):
		self.connect_to_mtgox_socket()
		while True:
			data = self.ws.recv()
			json_data = json.loads(data)
			print json_data
			self.publisher.publish(json.dumps(json_data), routing_key=json_data['channel_name'])