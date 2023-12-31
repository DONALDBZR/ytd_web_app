# Importing the system module
import sys
# Importing the logging module
import logging
# Inserting the application and packages
sys.path.insert(0, '/var/www/html/ytd_web_app')
sys.path.insert(0, '/var/www/html/ytd_web_app/venv/lib/python3.10/site-packages/')
# Setting up the logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# Import and run the application
from index import Application as application
