# Finding frequency of all categories in Raw Characteristics field to prepare full fix Dictionaries for next step forward
import pandas as pd
import json
import re

df = pd.read_csv("raw_characteristics_parsed_results.csv")

# Define multilingual aliases
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

# Robust parser
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

# Add target fields
for col in field_aliases.keys():
    df[col] = None

# Parse Raw Characteristics
for idx, row in df.iterrows():
    parsed = robust_safe_parse(row["Raw Characteristics"])
    for target_field, aliases in field_aliases.items():
        for alias in aliases:
            if alias in parsed:
                df.at[idx, target_field] = parsed[alias]
                break

# Normalize numeric values
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
print("✅ All features extracted → engineered_listings.csv")

