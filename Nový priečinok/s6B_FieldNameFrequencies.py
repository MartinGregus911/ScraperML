import pandas as pd
import ast
from s6Bb_field_aliases import field_aliases

# Load the parsed dataset
df = pd.read_csv("/data/debug/raw_characteristics_parsed_results.csv")

# Define field alias-based extractor
def extract_fields_from_raw(parsed_dict):
    extracted = {}
    for canonical_key, variants in field_aliases.items():
        for variant in variants:
            if variant in parsed_dict:
                extracted[canonical_key] = parsed_dict[variant]
                break
    return extracted

# Parse each row safely and extract features
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

# Convert to DataFrame and merge with original basic data
df_extracted = pd.DataFrame(extracted_rows)
df_final = pd.concat([df.drop(columns=["Raw Parsed"]), df_extracted], axis=1)

# Save the output
df_final.to_csv("/data/processed/engineered_listings.csv", index=False)
print(f"✅ Feature engineered listings saved. Total: {len(df_final)}")
