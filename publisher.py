import pika
import random
import time
import json

class Ticker():
	def __init__(self, publisher, qname):
		self.publisher = publisher
		self.stocks = ["MSFT", "AAPL", "YHOO", "LLOY"]
		self.last_quote = {}
		self.qname = qname

	def get_quote(self):
		stock = random.choice(self.stocks)
		if stock in self.last_quote:
			previous_quote = self.last_quote[stock]
			quote = random.uniform(0.99*previous_quote, 1.1*previous_quote)
		else:
			quote = random.uniform(30,250)
			self.last_quote[stock] = quote
		current_time = time.time()
		return {"stock": stock, "quote": quote, "current_time": current_time}

	def monitor(self):
		while True:
			quote = self.get_quote()
			self.publisher.publish(json.dumps(quote), routing_key=quote['stock'])