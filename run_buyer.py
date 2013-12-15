import sys

from rabbit.rabbitmqclient import *
publisher = PikaPublisher(exchange_name="ticker")

from buyer import * 
buyer = Buyer(publisher, "", 'depth.BTCUSD')
buyer.monitor()