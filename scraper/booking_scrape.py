import json
from booking_scraper import bkscraper

#It fetches only the first page for New York city with details


with open("output.json", 'w', encoding='utf-8') as f:
    for city in ['New York', 'Los Angeles']:
        result = bkscraper.get_result(city=city, limit=1, detail=True)
        json.dump(result, f, ensure_ascii=False, indent=4)
    f.close()