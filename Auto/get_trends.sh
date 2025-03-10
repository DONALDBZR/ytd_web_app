#!/bin/bash
# Xvfb :100 -screen 0 1366x768x24 &
# export DISPLAY=:100
source /home/darkness4869/Documents/extractio/venv/bin/activate
rm /home/darkness4869/Documents/extractio/Logs/Extractio.log
python3 /home/darkness4869/Documents/extractio/Auto/get_trends.py
# killall Xvfb
deactivate
