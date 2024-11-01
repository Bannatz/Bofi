import json
import os
import curses
import asyncio
from utils.player import Player
from utils.scraper import Scraper

class TUI:
    def __init__(self):
        self.player = Player()
        self.scraper = Scraper()
        self.song_list = []
        self.selected_song = 0
        self.top_line = 0

    async def fetch_songs(self):
        cache_file = 'song_cache.json'
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                self.song_list = json.load(f)
            print("Loaded songs from cache.")
        else:
            extension = "mp3"
            include_full = True
            year_filter = None
            month_filter = None
            self.song_list = await self.scraper.scan(extension, include_full, year_filter, month_filter)
            with open(cache_file, 'w') as f:
                json.dump(self.song_list, f)
            print("Fetched and cached songs.")

    async def load_and_play_song(self, url):
        await self.player.load_song_from_url(url)
        self.player.play_song()

    def display_interface(self, stdscr):
        stdscr.clear()
        curses.curs_set(0)

        stdscr.addstr(0, 0, "Fetching Songs, Please wait...")
        stdscr.refresh()

        asyncio.run(self.fetch_songs())
        stdscr.clear()

        max_y, max_x = stdscr.getmaxyx()  # Get terminal dimensions

        if not self.song_list:
            stdscr.addstr(0, 0, "No songs available.")
            stdscr.addstr(2, 0, "Press ESC to exit.")
            stdscr.refresh()
            stdscr.getch()  # Wait for user to acknowledge
            return

        # Calculate center position
        center_y = max_y // 2
        max_displayable_songs = max_y - 6  # Reserve space for title and controls
        half_displayable = max_displayable_songs // 2

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Bofi - Lofi Player", curses.A_BOLD)
            stdscr.addstr(2, 0, "Songs:")

            # Calculate the starting line to keep the selected song in the center
            if self.selected_song < half_displayable:
                self.top_line = 0
            elif self.selected_song > len(self.song_list) - half_displayable:
                self.top_line = len(self.song_list) - max_displayable_songs
            else:
                self.top_line = self.selected_song - half_displayable

            displayed_songs = self.song_list[self.top_line:self.top_line + max_displayable_songs]

            # Ensure we are not trying to print outside the bounds
            for idx, song_url in enumerate(displayed_songs):
                song_name = song_url.split('/')[-1]  # Get the song name from the URL
                display_name = song_name[:max_x - 4] + '...' if len(song_name) > max_x - 4 else song_name
                display_index = center_y + idx - (self.selected_song - self.top_line)

                # Ensure the display index is within valid bounds
                if 0 <= display_index < max_y:
                    if idx == self.selected_song - self.top_line:  # Adjust index to match displayed songs
                        stdscr.addstr(display_index, 0, f"> {display_name}", curses.A_REVERSE)
                    else:
                        stdscr.addstr(display_index, 0, f"  {display_name}")

            stdscr.addstr(max_y - 2, 0, "Use UP/DOWN to select a song, ENTER to Play, ESC to Exit")

            key = stdscr.getch()
            if key == curses.KEY_UP:
                if self.selected_song > 0:
                    self.selected_song -= 1
            elif key == curses.KEY_DOWN:
                if self.selected_song < len(self.song_list) - 1:
                    self.selected_song += 1
            elif key == ord("\n"):
                stdscr.clear()
                stdscr.addstr(0, 0, "Loading and Playing Song!")
                stdscr.refresh()
                song_url = self.song_list[self.selected_song]  # Get the URL
                asyncio.run(self.load_and_play_song(song_url))
            elif key == 27:  # ESC key to exit
                break

            stdscr.refresh()  # Refresh the screen to show changes

