import sys
from utils.scraper import Scraper
from utils.tui import TUI
import curses
import asyncio

sys.tracebacklimit = 1  # Suppress all Tracebacks.

def main():
    arg_len = len(sys.argv)

    if arg_len == 1:
        print("Usage: main.py <argument>")
        print("Commands:\nscrape [year_filter | month_filter]\nplayer - opens the music player")
        print("Example Usage: python main.py scrape [year_filter | month_filter]")
        return

    if sys.argv[1] == "scrape":
        # Set default values for year and month filters
        year_filter = None
        month_filter = None

        if arg_len >= 4:
            try:
                year_filter = int(sys.argv[2])  # Convert year filter to integer
                month_filter = sys.argv[3]  # Month filter remains a string
            except ValueError:
                print("Invalid Input: year_filter must be an integer.")
                return
        # Run the scrape function with the provided filters
        asyncio.run(Scraper().scrape("mp3", True, year_filter=year_filter, month_filter=month_filter))
    
    elif sys.argv[1] == "player":
            tui = TUI()
            curses.wrapper(tui.display_interface)

if __name__ == "__main__":
    main()

