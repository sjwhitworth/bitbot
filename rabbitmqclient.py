import pika

class PikaPublisher(object):
	def __init__(self, exchange_name):
		self.exchange_name = exchange_name
		self.queue_exists = False

	def publish(self, message, routing_key):
		connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		channel = connection.channel()
		channel.exchange_declare(exchange=self.exchange_name, type='direct')
		channel.basic_publish(exchange=self.exchange_name,
							  routing_key=routing_key,
							  body=message)
		channel.close()
		connection.close()

	def monitor(self, qname, callback, routing_key):
		connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		channel = connection.channel()

		if not self.queue_exists:
			channel.queue_declare(queue=qname)
			channel.queue_bind(queue=qname, exchange=self.exchange_name, routing_key=routing_key)
			self.queue_exists = True

		while True:
			channel.basic_consume(callback, queue=qname)