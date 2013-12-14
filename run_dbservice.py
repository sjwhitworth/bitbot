import sys

from rabbit.rabbitmqclient import *
service = PikaPublisher(exchange_name="ticker")

from db_service import * 
dbservice = DBService(service, "", sys.argv[1])
dbservice.monitor()