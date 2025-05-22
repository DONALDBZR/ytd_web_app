#!/bin/bash
source /home/darkness4869/Documents/extractio/venv/bin/activate
rm /home/darkness4869/Documents/extractio/Logs/Extractio.log
python3 /home/darkness4869/Documents/extractio/Auto/get_trends.py
deactivate
