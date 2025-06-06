import pandas as pd
import json

# Load cleaned listing data (raw parsed)
df_cleaned = pd.read_csv("final_cleaned_listings.csv")

# Load reference engineered listings with Listing ID
engineered = pd.read_csv("engineered_listings.csv")

# Build lookup from Raw Characteristics → Listing ID
raw_to_id = {}
for _, row in engineered.iterrows():
    raw = str(row["Raw Characteristics"]).strip()
    lid = row["Listing ID"]
    if raw and pd.notna(raw) and pd.notna(lid):
        raw_to_id[raw] = lid

# Inject Listing ID into cleaned data
def match_listing_id(raw):
    raw = str(raw).strip()
    return raw_to_id.get(raw, None)

df_cleaned["Listing ID"] = df_cleaned["Raw Characteristics"].apply(match_listing_id)

# Save to new file
df_cleaned.to_csv("final_cleaned_with_id.csv", index=False)
print("✅ Saved as final_cleaned_with_id.csv with Listing ID added.")
