# s6b_ExtractStructuredFeatures.py

import json
import re
import pandas as pd
from config import DEBUG_DIR, PROCESSED_DATA_DIR

# Input/output paths
input_file = DEBUG_DIR / "raw_characteristics_parsed_results.csv"
output_file = PROCESSED_DATA_DIR / "engineered_listings.csv"

# Load dataset
df = pd.read_csv(input_file)

# Define multilingual aliases (only yours, no extras)
field_aliases = {
    "Layout": ["Layout", "Dispozice", "Dispozícia"],
    "Floor": ["Floor", "Podlaží", "Poschodie"],
    "Užitná plocha": ["Užitná plocha", "Plocha kanceláře", "Plocha garáže", "Plocha nebytového prostoru", "Wohnfläche"],
    "Condition": ["Condition", "Stav", "Zustand"],
    "Building construction": ["Building construction", "Konstrukce budovy", "Bauart"],
    "EPC": ["EPC", "PENB"],
    "Location": ["Location", "Umístění", "Umiestnenie"],
    "Price per unit": ["Price per unit", "Cena za jednotku", "Cena za m2"]
}

# Safe JSON parser
def robust_safe_parse(raw):
    if pd.isna(raw):
        return {}
    try:
        return json.loads(raw)
    except Exception:
        try:
            cleaned = str(raw).replace('""', '"')
            cleaned = re.sub(r'^"|"$', '', cleaned)
            cleaned = cleaned.encode("utf-8").decode("unicode_escape")
            return json.loads(cleaned)
        except Exception:
            return {}

# Prepare empty target columns
for col in field_aliases:
    df[col] = None

# Extract values into normalized fields
for idx, row in df.iterrows():
    parsed = robust_safe_parse(row["Raw Characteristics"])
    for target_field, aliases in field_aliases.items():
        for alias in aliases:
            if alias in parsed:
                df.at[idx, target_field] = parsed[alias]
                break

# Parse and clean numeric fields
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

# Export engineered dataset
df.to_csv(output_file, index=False)
print("✅ All features extracted →", output_file.name)
