import pika
import json
import random

class Buyer(object):
	def __init__(self, client, qname, routing_key):
		self.qname = qname
		self.client = client
		self.routing_key = routing_key
		self.balance = 100000
		self.last_quote = {}
		self.holdings = {}
		self.history = {}

	def monitor(self):
		self.client.monitor(self.qname, self.handle_delivery, self.routing_key)

	def append_to_history(self, stock, quote):
		if stock not in self.history:
			self.history[stock] = [quote]
		else:
			self.history[stock].append(quote)

	def handle_delivery(self, ch, method, header, body):
		# print 'Received message:\n'
		# print body
		# print '----------\n'
		sanitised = json.loads(body)
		self.append_to_history(sanitised['stock'], sanitised['quote'])
		self.buy_or_sell(body, trend=3)

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

		if stock in self.holdings:
			if difference < 0:
				#print 'Difference is %s - going to buy' % difference
				amount = random.choice([5,100,30])
				self.holdings[stock] = float(amount)
				self.balance -= amount * quote
				#print 'I currently own %s shares of %s' % (self.holdings[stock], stock)

			elif difference > 0 and self.holdings[stock] > 0:
				#print 'Difference is %s - going to sell' % difference
				#print 'Potential profit of %s' % (self.holdings[stock] * quote,)
				valuation = self.holdings[stock] * quote
				self.balance += valuation
				self.holdings[stock] = 0
				#print valuation
		else:
			self.holdings[stock] = float(0)

		print self.balance

