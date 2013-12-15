import sys

from rabbit.rabbitmqclient import *
service = PikaPublisher(exchange_name="ticker")

from db_service import * 
dbservicedepth = DBService(service, "", 'depth.BTCUSD')
dbservice.monitor()