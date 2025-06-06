import pandas as pd

# Step 1: Load full list of intended listing URLs
with open("/data/raw/active_links_only.txt", "r", encoding="utf-8") as f:
    all_urls = [line.strip() for line in f.readlines()]

# Step 2: Load already scraped URLs from existing CSV
try:
    scraped_df = pd.read_csv("/data/raw/active_listings_with_prices_and_features.csv")
    scraped_urls = set(scraped_df["URL"])
except (FileNotFoundError, pd.errors.EmptyDataError):
    scraped_urls = set()  # If no file yet, nothing was scraped

# Step 3: Filter out already scraped URLs
remaining_urls = [url for url in all_urls if url not in scraped_urls]
print(f"🔍 Found {len(remaining_urls)} URLs to scrape (out of {len(all_urls)} total)")

# Step 4: Import the function to scrape each listing
from s3_ScrapeAllDataFromLinks import scrape_and_append_listing

# Step 5: Resume scraping only the missing ones
for url in remaining_urls:
    scrape_and_append_listing(url)
