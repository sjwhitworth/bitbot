import pika
import json
import random
from connection import Connection

class Buyer(Connection):
	def __init__(self, client, qname, routing_key):
		super(Buyer, self).__init__(client, qname, routing_key)
		self.balance = 100000
		self.last_quote = {}
		self.holdings = {}
		self.history = {}

	def handle_delivery(self, ch, method, header, body):
		sanitised = json.loads(body)
		self.append_to_history(sanitised['stock'], sanitised['quote'])
		self.buy_or_sell(body, trend=10)

	def append_to_history(self, stock, quote):
		if stock not in self.history:
			self.history[stock] = [quote]
		else:
			self.history[stock].append(quote)

	def buy_or_sell(self, message, trend=5):
		message = json.loads(message)
		stock, quote = message['stock'], float(message['quote'])

		if stock in self.last_quote:
			last_price  = self.last_quote[stock]
		else: 
			last_price = quote
			self.last_quote[stock] = quote

		difference = quote - last_price
		print '%s minute rolling average: %s' % (trend, sum(self.history[stock])/len(self.history[stock]))

