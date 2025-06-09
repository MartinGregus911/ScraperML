# s6c_AddListingID_viaRawCharacteristics.py

import pandas as pd
from config import PROCESSED_DATA_DIR

# Input/output
cleaned_file = PROCESSED_DATA_DIR / "s5_final_cleaned_listings.csv"
engineered_file = PROCESSED_DATA_DIR / "s6_engineered_listings.csv"
output_file = PROCESSED_DATA_DIR / "s6z_final_cleaned_with_id.csv"

# Load datasets
df_cleaned = pd.read_csv(cleaned_file)
df_engineered = pd.read_csv(engineered_file)

# Create temporary hash column to match listings
df_cleaned["_match_key"] = df_cleaned["Raw Characteristics"].astype(str).apply(hash)
df_engineered["_match_key"] = df_engineered["Raw Characteristics"].astype(str).apply(hash)

# Join on hash
merged = pd.merge(df_cleaned, df_engineered[["_match_key", "Listing ID"]], on="_match_key", how="left")

# Clean up
merged.drop(columns=["_match_key"], inplace=True)

# Save output as originally intended
merged.to_csv(output_file, index=False)
print(f"✅ Saved with Listing ID → {output_file.name}")
print(f"🆔 Matched: {merged['Listing ID'].notna().sum()} / {len(merged)}")
