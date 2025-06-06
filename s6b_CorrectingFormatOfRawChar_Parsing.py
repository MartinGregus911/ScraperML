import pandas as pd
import json
import re

def robust_safe_parse(raw):
    if pd.isna(raw):
        return {}

    try:
        # If it's already valid JSON, return it
        return json.loads(raw)
    except Exception:
        try:
            # Try to repair double-quoted JSON structure
            cleaned = str(raw).replace('""', '"')
            cleaned = re.sub(r'^"|"$', '', cleaned)  # remove wrapping quotes
            # Escape backslashes if present
            cleaned = cleaned.encode("utf-8").decode("unicode_escape")
            return json.loads(cleaned)
        except Exception:
            return {}

# Load full dataset
df = pd.read_csv("final_cleaned_listings.csv")

# Try to parse and track success
df["Raw Parsed"] = df["Raw Characteristics"].apply(robust_safe_parse)
df["Parse Success"] = df["Raw Parsed"].apply(lambda x: len(x) > 0)

valid_count = df["Parse Success"].sum()
invalid_count = (~df["Parse Success"]).sum()

print(f"🟢 JSON parsed successfully: {valid_count}")
print(f"🔴 Still broken: {invalid_count}")

# Optional: save results to inspect if needed
df[["Raw Characteristics", "Raw Parsed", "Parse Success"]].to_csv("raw_characteristics_parsed_results.csv", index=False)
