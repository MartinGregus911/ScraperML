# s3b_ResumeScrap_restored.py

import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import re
import json
import pandas as pd

# Import config
sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import RAW_DATA_DIR

headers = {"User-Agent": "Mozilla/5.0"}

INPUT_FILE = RAW_DATA_DIR / "s2_active_links_checked.txt"
OUTPUT_FILE = RAW_DATA_DIR / "s3_active_listings_with_prices_and_features.csv"
FAILED_LOG = RAW_DATA_DIR / "s3b_failed_urls_resume.txt"

columns = [
    "Title", "URL", "Listing Type", "Base Price", "Discount", "Original Price",
    "Monthly Rent", "Service Charges", "Utility Charges", "Administrative Fee",
    "Refundable Deposit", "Raw Characteristics"
]

# Load input URLs
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    all_urls = [line.strip().rstrip("/") for line in f if line.strip()]

# Load already-scraped URLs from CSV
try:
    df_existing = pd.read_csv(OUTPUT_FILE, usecols=["URL"])
    scraped_urls = set(df_existing["URL"].dropna().astype(str).str.strip().str.rstrip("/"))
except Exception as e:
    print(f"⚠️ Could not load scraped URLs: {e}")
    scraped_urls = set()

# Compute remaining
remaining_urls = [url for url in all_urls if url not in scraped_urls]
total = len(remaining_urls)

print(f"🔍 Total input: {len(all_urls)} | ✅ Already scraped: {len(scraped_urls)} | 🚧 Remaining: {total}")

def clean_price(text):
    return re.sub(r"[^0-9€$CZK]", "", text).strip()

def get_text_or_na(tag):
    return tag.get_text(strip=True) if tag else "N/A"

# Resume scrape loop
with open(OUTPUT_FILE, "a", encoding="utf-8", newline="") as f_out:
    writer = csv.writer(f_out)

    for idx, url in enumerate(remaining_urls, start=1):
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            title_tag = soup.find("h1")
            title = get_text_or_na(title_tag)

            page_text = soup.get_text().lower()
            listing_type = "Rent" if "monthly rent" in page_text else ("Sale" if "price" in page_text else "Unknown")

            base_price = discount = original_price = monthly_rent = service = utility = admin_fee = deposit = "N/A"

            if listing_type == "Sale":
                price_tag = soup.find("span", string="Price")
                if price_tag:
                    strong_tag = price_tag.find_next("strong", class_="h4 fw-bold")
                    if strong_tag and strong_tag.find("span"):
                        base_price = clean_price(strong_tag.find("span").text)

                save_tag = soup.find(string=re.compile("Save"))
                if save_tag:
                    discount_span = save_tag.find_next("span")
                    if discount_span:
                        discount = clean_price(discount_span.text)

                original_tag = soup.find(class_="StickyBox_stickyBoxPriceOriginal__eyrS7")
                if original_tag:
                    span = original_tag.find("span")
                    if span:
                        original_price = clean_price(span.text)

            elif listing_type == "Rent":
                rent_tag = soup.find("span", string="Monthly rent")
                if rent_tag:
                    price_span = rent_tag.find_next("strong", class_="h4 fw-bold").find("span")
                    if price_span:
                        monthly_rent = clean_price(price_span.text)

                def extract_extra(label):
                    tag = soup.find("span", string=re.compile(re.escape(label), re.I))
                    if tag:
                        val_tag = tag.find_next("strong")
                        if val_tag and val_tag.find("span"):
                            return clean_price(val_tag.find("span").text)
                    return "N/A"

                service = extract_extra("Service charges")
                utility = extract_extra("Utility charges")
                admin_fee = extract_extra("Administrative fee")
                deposit = extract_extra("Refundable deposit")

            raw_characteristics = {}
            section = soup.find("h2", string="Property Characteristics")
            if section:
                tables = section.find_all_next("table")
                for table in tables:
                    rows = table.find_all("tr")
                    for row in rows:
                        th = row.find("th")
                        td = row.find("td")
                        if th and td:
                            key = th.get_text(strip=True)
                            value = td.get_text(strip=True)
                            raw_characteristics[key] = value

            writer.writerow([
                title, url, listing_type, base_price, discount, original_price,
                monthly_rent, service, utility, admin_fee, deposit,
                json.dumps(raw_characteristics, ensure_ascii=False)
            ])

            print(f"[{idx:05}/{total}] ✅ Resumed: {url}")
            time.sleep(random.uniform(0.3, 0.6))

        except Exception as e:
            print(f"[{idx:05}/{total}] ⚠️ Failed: {url} — {e}")
            with open(FAILED_LOG, "a", encoding="utf-8") as f_log:
                f_log.write(f"{url} - {e}\n")
