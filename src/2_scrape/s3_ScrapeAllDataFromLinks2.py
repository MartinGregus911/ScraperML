# s3_ScrapeAllDataFromLinks_restored.py

import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import re
import json

# Allow import of config from root
sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import RAW_DATA_DIR

headers = {"User-Agent": "Mozilla/5.0"}

def clean_price(text):
    return re.sub(r"[^0-9€$CZK]", "", text).strip()

def get_text_or_na(tag):
    return tag.get_text(strip=True) if tag else "N/A"

# Load all active links
input_path = RAW_DATA_DIR / "s2_active_links_checked.txt"
with open(input_path, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]
total = len(urls)

# Prepare output
output_path = RAW_DATA_DIR / "s3_active_listings_with_prices_and_features.csv"
with open(output_path, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.writer(f_out)
    writer.writerow([
        "Title", "URL", "Listing Type", "Base Price", "Discount", "Original Price",
        "Monthly Rent", "Service Charges", "Utility Charges", "Administrative Fee",
        "Refundable Deposit", "Raw Characteristics"
    ])

    for idx, url in enumerate(urls, start=1):
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            title_tag = soup.find("h1")
            title = get_text_or_na(title_tag)

            # Rent or Sale determination
            page_text = soup.get_text().lower()
            listing_type = "Rent" if "monthly rent" in page_text else ("Sale" if "price" in page_text else "Unknown")

            # Default placeholders
            base_price = discount = original_price = monthly_rent = service = utility = admin_fee = deposit = "N/A"

            if listing_type == "Sale":
                price_tag = soup.find("span", string="Price")
                if price_tag:
                    strong = price_tag.find_next("strong", class_="h4 fw-bold")
                    if strong and strong.find("span"):
                        base_price = clean_price(strong.find("span").text)

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

            # Raw Characteristics (from Property Characteristics section)
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

            # Write to output
            writer.writerow([
                title, url, listing_type, base_price, discount, original_price,
                monthly_rent, service, utility, admin_fee, deposit,
                json.dumps(raw_characteristics, ensure_ascii=False)
            ])

            print(f"[{idx:05}/{total}] ✅ Scraped: {url}")
            time.sleep(random.uniform(0.3, 0.6))

        except Exception as e:
            print(f"[{idx:05}/{total}] ⚠️ Failed: {url} — {e}")
            continue
