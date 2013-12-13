from rabbitmqclient import *
publisher = PikaPublisher(exchange_name="ticker")

from publisher import *
ticker = Ticker(publisher, "")
ticker.monitor()