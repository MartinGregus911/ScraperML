import pandas as pd
import json
import random
import re

df = pd.read_csv("/data/processed/final_cleaned_listings.csv")

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

def safe_parse(raw):
    try:
        cleaned = re.sub(r'""', '"', str(raw))
        cleaned = re.sub(r'"{2,}', '"', cleaned)
        return json.loads(cleaned)
    except Exception:
        return {}

sample = df.sample(5000, random_state=42)
logs = []

for _, row in sample.iterrows():
    parsed = safe_parse(row["Raw Characteristics"])
    keys_found = list(parsed.keys())
    matched = {}
    for target_field, aliases in field_aliases.items():
        match = next((alias for alias in aliases if alias in parsed), None)
        matched[target_field] = match if match else "❌ No match"
    logs.append({
        "Title": row.get("Title", "N/A"),
        "Keys Found": keys_found,
        "Field Matches": matched
    })

debug_df = pd.DataFrame(logs)
debug_df.to_csv("/data/debug/debug_feature_extraction_50.csv", index=False)
print("🔍 Debug results saved to debug_feature_extraction_50.csv")

