"""
Hotels Extract — Booking.com (one-time Scrapy spider)
"""

import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import os


class HotelsSpider(scrapy.Spider):
    name = "hotels_description"

    # Predefined list of locations
    locations = [
        "Le+Mont-Saint-Michel",
        "Saint-Malo",
        "Bayeux",
        "Le+Havre",
        "Rouen",
        "Paris",
        "Amiens",
        "Lille",
        "Strasbourg",
        "Chateau+du+Haut+Koenigsbourg",
        "Colmar",
        "Eguisheim",
        "Besancon",
        "Dijon",
        "Annecy",
        "Grenoble",
        "Lyon",
        "Gorges+du+Verdon",
        "Bormes+les+Mimosas",
        "Cassis",
        "Marseille",
        "Aix+en+Provence",
        "Avignon",
        "Uzes",
        "Nîmes",
        "Aigues+Mortes",
        "Saintes+Maries+de+la+mer",
        "Collioure",
        "Carcassonne",
        "Ariege",
        "Toulouse",
        "Montauban",
        "Biarritz",
        "Bayonne",
        "La+Rochelle",
    ]

    # Build search result URLs for each location
    start_urls = [
        f"https://www.booking.com/searchresults.fr.html?ss={location}" for location in locations
    ]

    def parse(self, response):
        """Parse the hotel list page for one location."""
        location = response.url.split("ss=")[-1].replace("+", " ")
        hotels = response.css('div[data-testid="property-card"]')

        for hotel in hotels:
            name = hotel.css('div[data-testid="title"]::text').get()
            url = hotel.css('a[data-testid="title-link"]::attr(href)').get()
            rating = hotel.css("div[class='a3b8729ab1 d86cee9b25']::text").get()

            if url:
                # Follow each hotel page to extract details
                yield response.follow(
                    url,
                    callback=self.parse_hotel,
                    meta={
                        "location": location,
                        "name": name.strip() if name else None,
                        "rating": rating,
                    },
                )

    def parse_hotel(self, response):
        """Parse a hotel detail page to extract description and coordinates."""
        description = response.css('p[data-testid="property-description"]::text').get()
        coord = response.xpath("//*[@data-atlas-latlng]/@data-atlas-latlng").get()

        yield {
            "location": response.meta["location"],
            "name": response.meta["name"],
            "rating": response.meta["rating"],
            "url": response.url,
            "description": description.strip() if description else None,
            "coordinates": coord,
        }


# Write output under <script_dir>/data/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)  # create if missing

filename = os.path.join(DATA_DIR, "hotels_descriptions.json")

# Delete the file if it already exists (avoid appending old data)
if os.path.exists(filename):
    os.remove(filename)

# Configure Scrapy process
process = CrawlerProcess(
    settings={
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "LOG_LEVEL": logging.INFO,
        "FEEDS": {
            filename: {"format": "json", "encoding": "utf8", "indent": 4},
        },
    }
)

# Start the spider
process.crawl(HotelsSpider)
process.start()
