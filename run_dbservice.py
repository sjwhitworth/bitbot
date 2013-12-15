import sys

from rabbit.rabbitmqclient import *
service = PikaPublisher(exchange_name="ticker")

from db_service import * 
dbservice = DBService(service, "", 'depth.BTCUSD')
dbservice.monitor()