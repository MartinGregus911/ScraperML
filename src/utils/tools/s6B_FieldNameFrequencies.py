# s6_MainFeatureEngineering_B.py

import ast
import pandas as pd
from config import DEBUG_DIR
from src.utils.mappings.s6b_field_aliases import field_aliases

# Load parsed raw characteristics
input_file = DEBUG_DIR / "s6b_raw_characteristics_parsed_results.csv"
df = pd.read_csv(input_file)

# Define alias-based extractor
def extract_fields_from_raw(parsed_dict):
    extracted = {}
    for canonical_key, variants in field_aliases.items():
        for variant in variants:
            if variant in parsed_dict:
                extracted[canonical_key] = parsed_dict[variant]
                break
    return extracted

# Safely evaluate parsed JSON strings and extract fields
extracted_rows = []

for raw in df["Raw Parsed"]:
    try:
        parsed_dict = ast.literal_eval(raw)
        if isinstance(parsed_dict, dict):
            extracted = extract_fields_from_raw(parsed_dict)
            extracted_rows.append(extracted)
        else:
            extracted_rows.append({})
    except:
        extracted_rows.append({})

# Combine with base data
df_extracted = pd.DataFrame(extracted_rows)
df_final = pd.concat([df.drop(columns=["Raw Parsed"]), df_extracted], axis=1)

# Save final output
output_file = DEBUG_DIR / "s6B_engineered_listing_field_frequency_debug.csv"
df_final.to_csv(output_file, index=False)

print(f"✅ Feature engineered listings saved. Total: {len(df_final)}")
