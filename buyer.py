import pika
import json
import random
from connection import Connection

market_depth = {}

class Buyer(Connection):
	def __init__(self, client, qname, routing_key):
		super(Buyer, self).__init__(client, qname, routing_key)
		self.balance = 100000
		self.last_quote = {}
		self.holdings = {}
		self.history = {}

	def handle_delivery(self, ch, method, header, body):
		sanitised = json.loads(body)
		self.update_market_depth(sanitised)

	def update_market_depth(self, data):
		depth = data['depth']
		if depth['price'] not in market_depth:
			market_depth[depth['price']] = depth['total_volume_int']
		else:
			market_depth[depth['price']] = depth['total_volume_int']

