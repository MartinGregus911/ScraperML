import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import os

# Output file
OUTPUT_FILE = "data/raw/active_listings_with_prices_and_features.csv"
CSV_COLUMNS = [
    "Title", "URL", "Listing Type", "Base Price", "Discount", "Original Price",
    "Monthly Rent", "Service Charges", "Utility Charges", "Administrative Fee",
    "Refundable Deposit", "Raw Characteristics"
]

# Make sure CSV exists and has headers
if not os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)

def scrape_and_append_listing(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # ⬇️ Replace this section with your real parsing logic:
        title = soup.title.text.strip()
        # Example: Extract fields based on known page structure
        listing_type = "Rent" if "pronajem" in url else "Sale"
        base_price = "CZK8000"  # dummy fallback

        row = [
            title, url, listing_type, base_price, "", "", "", "", "", "", "", "{}"
        ]

        # Append the row to the CSV
        with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        print(f"✅ Scraped: {url}")

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"❌ Skipping missing listing (404): {url}")
        else:
            print(f"⚠️ HTTP error {response.status_code}: {url}")
            with open("failed_urls.txt", "a") as f:
                f.write(f"{url} - {response.status_code}\n")
    except Exception as e:
        print(f"⚠️ Error at {url}: {e}")
        with open("failed_urls.txt", "a") as f:
            f.write(f"{url} - Exception: {e}\n")

# Optional: standalone usage
if __name__ == "__main__":
    with open("data/raw/active_links_only.txt", "r") as f:
        urls = [line.strip() for line in f.readlines()]
    for url in urls:
        scrape_and_append_listing(url)
