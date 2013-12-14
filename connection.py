import pika
import json

class Connection(object):
	def __init__(self, client, qname, routing_key):
		self.qname = qname
		self.client = client
		self.routing_key = routing_key

	def monitor(self):
		self.client.monitor(self.qname, self.handle_delivery, self.routing_key)