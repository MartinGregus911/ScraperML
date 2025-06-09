# s1_ExtractAllLinksToTxt.py
import requests
from bs4 import BeautifulSoup
from config import RAW_DATA_DIR

sitemap_urls = [
    "https://www.bezrealitky.com/sitemap/sitemap_detail_1.xml",
    "https://www.bezrealitky.com/sitemap/sitemap_detail_2.xml",
    "https://www.bezrealitky.com/sitemap/sitemap_detail_3.xml",
    "https://www.bezrealitky.com/sitemap/sitemap_detail_4.xml",
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

output_path = RAW_DATA_DIR / "s1_all_listing_links.txt"
with open(output_path, "w", encoding="utf-8") as f:
    for link in filtered_links:
        f.write(link + "\n")

print(f"🌐 Sitemaps total links: {len(all_links)}")
print(f"✅ Saved filtered property links: {len(filtered_links)}")
