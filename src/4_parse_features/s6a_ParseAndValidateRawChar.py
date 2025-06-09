# s6b_TestRobustSafeParse.py

import json
import re
import pandas as pd
from config import PROCESSED_DATA_DIR, DEBUG_DIR

# Robust parser for JSON in Raw Characteristics
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

# Load full dataset
input_file = PROCESSED_DATA_DIR / "s5_final_cleaned_listings.csv"
df = pd.read_csv(input_file)

# Apply parser
df["Raw Parsed"] = df["Raw Characteristics"].apply(robust_safe_parse)
df["Parse Success"] = df["Raw Parsed"].apply(lambda x: len(x) > 0)

# Summary
valid_count = df["Parse Success"].sum()
invalid_count = (~df["Parse Success"]).sum()
print(f"🟢 JSON parsed successfully: {valid_count}")
print(f"🔴 Still broken: {invalid_count}")

# Save debug output
output_file = DEBUG_DIR / "s6b_raw_characteristics_parsed_results.csv"
df[["Raw Characteristics", "Raw Parsed", "Parse Success"]].to_csv(output_file, index=False)
print("✅ Saved parsed results to:", output_file.name)
