#!/usr/bin/env bash
python2.7 run_publisher.py &
sleep 10 &&
python2.7 run_buyer.py &
python2.7 run_dbservice.py