from connection import Connection
import psycopg2
import json
from config import DBNAME, PORT, HOST, USER, PASSWORD
import time

class DBService(Connection):
	def handle_delivery(self, ch, method, header, body):
		sanitised = json.loads(body)
		self.insert_market_depth(sanitised['depth'])

	def connect_to_database(self, port, dbname, host, user, password):
		self.conn = psycopg2.connect(database=dbname, host=host,
								  port=port, user=user, 
								  password=password)
		self.conn.autocommit = True
		self.cur = self.conn.cursor()

	def insert_market_depth(self, data):
		self.cur.execute("INSERT INTO market_depth VALUES (%s, %s, %s)", 
						 (data['total_volume_int'], data['price'], int(time.time())))

	def monitor(self):
		self.connect_to_database(port=PORT, dbname=DBNAME, 
								 host=HOST, user=USER,
								 password=PASSWORD)
		while True:
			self.client.monitor(self.qname, self.handle_delivery, self.routing_key)

