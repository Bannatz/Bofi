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
        curses.curs_set(0)  # Hide the cursor

        stdscr.addstr(0, 0, "Fetching Songs, Please wait...")
        stdscr.refresh()

        asyncio.run(self.fetch_songs())
        stdscr.clear()

        if not self.song_list:
            stdscr.addstr(0, 0, "No songs available.")
            stdscr.addstr(2, 0, "Press ESC to exit.")
            stdscr.refresh()
            stdscr.getch()
            return

        # Initialize song selection and top line
        self.selected_song = 0
        self.top_line = 0

        # Create windows once
        max_y, max_x = stdscr.getmaxyx()
        title_space = 1
        control_space = 4
        song_window_height = max_y - title_space - control_space - 2

        if song_window_height <= 0:
            stdscr.addstr(0, 0, "Terminal height is too small for the song list.")
            stdscr.refresh()
            stdscr.getch()
            return

        # Create the song window once
        song_window = curses.newwin(song_window_height, max_x, title_space + 1, 0)
        
        def draw_screen():
            # Draw title
            stdscr.addstr(0, 0, "Bofi - Lofi Player", curses.A_BOLD)
            stdscr.addstr(1, 0, "-" * (max_x - 1))

            # Draw song window
            song_window.erase()
            song_window.box()

            # Calculate visible space
            visible_space = song_window_height - 2

            # Display songs
            for idx in range(visible_space):
                current_song_idx = self.top_line + idx
                if current_song_idx < len(self.song_list):
                    song_url = self.song_list[current_song_idx]
                    song_name = song_url.split('/')[-1]

                    # Truncate song name if needed
                    max_song_width = max_x - 6
                    if len(song_name) > max_song_width:
                        song_name = song_name[:max_song_width - 3] + "..."

                    try:
                        selection_marker = '>' if current_song_idx == self.selected_song else ' '
                        song_window.addstr(
                            idx + 1,
                            2,
                            f"{selection_marker} {song_name}",
                            curses.A_REVERSE if current_song_idx == self.selected_song else curses.A_NORMAL
                        )
                    except curses.error:
                        pass

            # Draw controls
            try:
                controls_y = max_y - control_space
                stdscr.addstr(controls_y, 0, "-" * (max_x - 1))
                stdscr.addstr(controls_y + 1, 0, f"Volume: {int(self.player.volume * 100)}%")
                stdscr.addstr(controls_y + 2, 0, "Use +/- to Increase or Decrease Volume!")
                stdscr.addstr(controls_y + 3, 0, "Use UP/DOWN to select a song, ENTER to Play, ESC to Exit")
            except curses.error:
                pass

            # Refresh windows
            stdscr.refresh()
            song_window.refresh()

        # Main loop
        while True:
            # Draw everything
            draw_screen()

            # Handle input
            key = stdscr.getch()
            visible_space = song_window_height - 2
            
            if key == curses.KEY_UP:
                if self.selected_song > 0:
                    self.selected_song -= 1
                    if self.selected_song < self.top_line:
                        self.top_line = self.selected_song
            elif key == curses.KEY_DOWN:
                if self.selected_song < len(self.song_list) - 1:
                    self.selected_song += 1
                    if self.selected_song >= self.top_line + visible_space:
                        self.top_line = self.selected_song - visible_space + 1     
            elif key == ord("+"):
                self.player.increase_volume()
            elif key == ord("-"):
                self.player.decrease_volume()
            elif key == ord("\n"):
                stdscr.clear()
                stdscr.addstr(0, 0, "Loading and Playing Song!")
                stdscr.refresh()
                song_url = self.song_list[self.selected_song]
                asyncio.run(self.load_and_play_song(song_url))
                # Redraw everything after playing
                stdscr.clear()
                draw_screen()
            elif key == 27:  # ESC
                break


