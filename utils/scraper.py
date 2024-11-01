import aiohttp
import asyncio
from bs4 import BeautifulSoup as bs4
from typing import List, Optional
import json

class Scraper:
    def __init__(self):
        self.base_url = "https://lofigirl.com/wp-content/uploads/"
        self.volume = 50

    async def parse(self, path: str) -> List[str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}{path}") as resp:
                document = await resp.text()
                soup = bs4(document, "html.parser")
                links = soup.select("html > body > pre > a")
                return [link.get("href") for link in links[5:]]

    def set_volume(self, volume):
        self.volume = max(0 , min(volume, 100))
        print(f"Volume set to {self.volume}")

    def increase_volume(self):
        self.set_volume(self.volume + 5)
    
    def decrease_volume(self):
        self.set_volume(self.volume -5)

    async def scan(self, extension: str, include_full: bool, year_filter: Optional[int] = None, month_filter: Optional[str] = None) -> List[str]:
        # Check for cached data
        try:
            with open("cache.json", 'r') as f:
                cached_data = json.load(f)
                print("Loaded songs from cache.")
                for song in cached_data:
                    print(f"{song}")
                return cached_data  # Return cached data if it exists
        except FileNotFoundError:
            print("No cache found, scraping...")

        extension = f".{extension}"
        items = await self.parse("")

        years = [int(x[:-1]) for x in items if x.endswith("/") and x[:-1].isdigit()]
        files = []

        async def fetch_months(year: int):
            months = await self.parse(str(year))
            print(f"Year: {year}, Available months: {months}")
            for month in months:
                if month_filter and month.replace("/", "") != month_filter:
                    continue
                path = f"{year}/{month}"
                print(f"Fetching path: {path}")
                items = await self.parse(path)
                for x in items:
                    if x.endswith(extension):
                        full_path = f"{self.base_url}{path}{x}" if include_full else f"{path}{x}"
                        files.append(full_path)

        tasks = [fetch_months(year) for year in years if not year_filter or year == year_filter]
        await asyncio.gather(*tasks)

        with open("cache.json", "w") as f:
            json.dump(files, f)

        return files

    async def scrape(self, extension: str, include_full: bool, year_filter: Optional[int], month_filter: Optional[str]) -> None:
        files = await self.scan(extension, include_full, year_filter, month_filter)
        for file in files:
            print(file)

