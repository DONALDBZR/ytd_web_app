import os
import sys


models_directory = f"{os.getcwd()}/Models"
sys.path.insert(0, models_directory)

from Crawler import Crawler


web_scraper = Crawler()