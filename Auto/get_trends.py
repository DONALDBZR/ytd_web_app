from sys import exit
from Classes.Crawler import Crawler


crawler = None
try:
    crawler = Crawler()
    outcome = crawler.getOutcome()
except Exception:
    outcome = "failed"
finally:
    if crawler is not None:
        crawler.close()
exit(1 if outcome == "failed" else 0)
