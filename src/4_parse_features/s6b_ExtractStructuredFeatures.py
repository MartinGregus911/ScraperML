# s6b_MainFeatureEngineering.py

import json
import re
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import DEBUG_DIR, PROCESSED_DATA_DIR
from src.utils.mappings.s6b_field_aliases import field_aliases

# Input/output
input_file = DEBUG_DIR / "s6b_raw_characteristics_parsed_results.csv"
output_file = PROCESSED_DATA_DIR / "s6_engineered_listings.csv"

df = pd.read_csv(input_file)

# Add columns
for col in field_aliases:
    df[col] = None

# Extract values
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

for idx, row in df.iterrows():
    parsed = robust_safe_parse(row["Raw Characteristics"])
    for target_field, aliases in field_aliases.items():
        for alias in aliases:
            if alias in parsed:
                df.at[idx, target_field] = parsed[alias]
                break

# Normalize numeric fields
def extract_number(value):
    if pd.isna(value):
        return None
    value = re.sub(r"[^\d.]", "", str(value).replace(",", "."))
    try:
        return float(value)
    except ValueError:
        return None

if "Užitná plocha" in df.columns:
    df["Užitná plocha"] = df["Užitná plocha"].apply(extract_number)
if "Price per unit" in df.columns:
    df["Price per unit"] = df["Price per unit"].apply(extract_number)

df.to_csv(output_file, index=False)
print("✅ All features extracted →", output_file.name)
