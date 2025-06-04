import pandas as pd
import json
import re

df = pd.read_csv("cleaned_listings.csv")

fields_to_extract = [
    "Layout",
    "Floor",
    "Užitná plocha",
    "Condition",
    "Building construction",
    "EPC",
    "Location",
    "Price per unit"
]

# Add new columns with default None
for field in fields_to_extract:
    df[field] = None

# Safe JSON cleaner
def safe_parse(raw):
    try:
        cleaned = re.sub(r'""', '"', str(raw))
        cleaned = re.sub(r'"{2,}', '"', cleaned)  # replace repeated quotes
        cleaned = re.sub(r'"\s*:\s*"', lambda m: m.group(0) if ":" in m.group(0) else '', cleaned)
        return json.loads(cleaned)
    except Exception:
        return {}

# Parse and extract
for idx, row in df.iterrows():
    characteristics = safe_parse(row["Raw Characteristics"])
    for field in fields_to_extract:
        if field in characteristics:
            df.at[idx, field] = characteristics[field]

# Normalize numeric fields
def extract_number(value):
    if pd.isna(value):
        return None
    value = re.sub(r"[^\d.]", "", str(value).replace(",", "."))
    try:
        return float(value)
    except ValueError:
        return None

df["Užitná plocha"] = df["Užitná plocha"].apply(extract_number)
df["Price per unit"] = df["Price per unit"].apply(extract_number)

df.to_csv("engineered_listings.csv", index=False)

print("✅ Feature Engineering complete → engineered_listings.csv saved.")
