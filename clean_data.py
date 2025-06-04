import pandas as pd
import os
import re

# Input and output paths
INPUT_FILE = "active_listings_with_prices_and_features.csv"
OUTPUT_DIR = "data/processed"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "listings_clean.csv")

# Make sure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data
df = pd.read_csv(INPUT_FILE)

# ========== FIELD PARSING LOGIC ==========

# 1. Parse price (Monthly Rent or Base Price)
def parse_price(row):
    # Prioritize Monthly Rent, then Base Price
    for field in ["Monthly Rent", "Base Price", "Original Price"]:
        value = str(row.get(field, "")).replace("CZK", "").replace(",", "").strip()
        try:
            return float(re.search(r"[\d\.]+", value).group())
        except:
            continue
    return None

df["price_eur"] = df.apply(parse_price, axis=1)

# 2. Parse size (m²)
def extract_size(row):
    rc = str(row.get("Raw Characteristics", ""))
    match = re.search(r'(\d+(?:[\s,]?\d+)*)\s?m²', rc)
    if match:
        return float(match.group(1).replace(" ", "").replace(",", ""))
    return None

df["size_m2"] = df.apply(extract_size, axis=1)

# 3. Parse floor
def extract_floor(row):
    rc = str(row.get("Raw Characteristics", ""))
    match = re.search(r'(\d+)\. podla[zž]í', rc)
    if match:
        return int(match.group(1))
    elif "Ground floor" in rc:
        return 0
    return None

df["floor"] = df.apply(extract_floor, axis=1)

# 4. Add placeholder for location (could parse later from Title)
df["location"] = df["Title"].str.extract(r'•.*?([\w\s\-\,]+)$', expand=False).str.strip()

# 5. Drop rows with missing essential values
df_clean = df.dropna(subset=["price_eur", "size_m2"])

# Save cleaned data
df_clean.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Cleaned data saved to: {OUTPUT_FILE}")
