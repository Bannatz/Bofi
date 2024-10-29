import sys
from utils.scraper.py import Scraper
sys.tracebacklimit = 0 # Suppress all Tracebacks.

def main():
    arg_len = len(sys.argv)
    if arg_len == 1:
        print("Usage: main.py <argument>")
        print("help - prints this message.\nscrape <single | album | website> - only scrapes the given second argument.\nplay [single | album]")
        print("Example: python main.py scrape album")
        return
    if sys.argv[1] == "scrape":
        Scraper.scrape()
main()
