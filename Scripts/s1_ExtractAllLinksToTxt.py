import requests
from bs4 import BeautifulSoup
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
output_file = ROOT / "data" / "raw" / "all_listing_links.txt"

sitemap_urls = [
    "https://www.bezrealitky.com/sitemap/sitemap_detail_1.xml",
    "https://www.bezrealitky.com/sitemap/sitemap_detail_2.xml",
    "https://www.bezrealitky.com/sitemap/sitemap_detail_3.xml",
    "https://www.bezrealitky.com/sitemap/sitemap_detail_4.xml"
]

all_links = []

for sitemap in sitemap_urls:
    res = requests.get(sitemap)
    soup = BeautifulSoup(res.text, "xml")
    links = [loc.text for loc in soup.find_all("loc")]
    all_links.extend(links)

filtered_links = [
    url for url in all_links
    if url.startswith("https://www.bezrealitky.com/properties-flats-houses/")
]

output_file.parent.mkdir(parents=True, exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    for link in filtered_links:
        f.write(link + "\n")

print("Saved filtered links:", len(filtered_links))
