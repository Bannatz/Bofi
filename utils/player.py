import aiohttp
import asyncio
import io
from pydub import AudioSegment
import pygame

class Player:
    def __init__(self):
        self.current_song = None
        pygame.mixer.init()

    async def load_song_from_url(self, url):
        try:
            print(f"Downloading song from {url}...")
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        audio_data = io.BytesIO(await resp.read())
                        self.current_song = AudioSegment.from_file(audio_data, format="mp3")
                        temp_wav = io.BytesIO()
                        self.current_song.export(temp_wav, format="wav")
                        temp_wav.seek(0)
                        pygame.mixer.music.load(temp_wav)
                        print("Song downloaded and loaded successfully.")
                    else:
                        print(f"Failed to get the song: HTTP {resp.status}")
        except Exception as e:
            print(f"Error loading song: {e}")

    def play_song(self):
        if self.current_song:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop() 
            pygame.mixer.music.play()
            print("Playing song...")
        else:
            print("No song loaded to play.")

    def stop_song(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            print("Stopped playback.")
