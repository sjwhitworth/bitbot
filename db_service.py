from connection import Connection
import psycopg2
import json
from config import DBNAME, PORT, HOST, USER, PASSWORD

class DBService(Connection):
	def handle_delivery(self, ch, method, header, body):
		sanitised = json.loads(body)
		self.cur.execute("INSERT INTO prices VALUES (%s, %s, %s)", 
						 (sanitised['current_time'], sanitised['quote'], sanitised['stock']))

	def connect_to_database(self, port, dbname, host, user, password):
		self.conn = psycopg2.connect(database=dbname, host=host,
								  port=port, user=user, 
								  password=password)
		self.conn.autocommit = True
		self.cur = self.conn.cursor()

	def monitor(self):
		self.connect_to_database(port=PORT, dbname=DBNAME, 
								 host=HOST, user=USER,
								 password=PASSWORD)
		while True:
			self.client.monitor(self.qname, self.handle_delivery, self.routing_key)

