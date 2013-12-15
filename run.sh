#!/usr/bin/env bash
python run_publisher.py &
sleep 10 &&
python run_buyer.py &
python run_dbservice.py