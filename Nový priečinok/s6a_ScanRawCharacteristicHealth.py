import pandas as pd
import json
import re

df = pd.read_csv("/data/processed/final_cleaned_listings.csv")

def is_valid_json(raw):
    try:
        cleaned = re.sub(r'""', '"', str(raw))
        cleaned = re.sub(r'"{2,}', '"', cleaned)
        json.loads(cleaned)
        return True
    except:
        return False

df["is_valid_json"] = df["Raw Characteristics"].apply(is_valid_json)

valid_count = df["is_valid_json"].sum()
invalid_count = (~df["is_valid_json"]).sum()

print(f"✅ Valid JSON rows: {valid_count}")
print(f"❌ Invalid JSON rows: {invalid_count}")

# Save a sample of invalid ones
invalid_samples = df[~df["is_valid_json"]]["Raw Characteristics"].dropna().sample(15, random_state=42)
invalid_samples.to_csv("/data/debug/raw_characteristics_invalid_sample.csv", index=False)
print("📄 Saved 15 invalid samples to raw_characteristics_invalid_sample.csv")