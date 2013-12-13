import sys

from rabbitmqclient import *
publisher = PikaPublisher(exchange_name="ticker")

from buyer import * 
buyer = Buyer(publisher, "", sys.argv[1])
buyer.monitor()