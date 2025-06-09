# s7zz_CleanEngineeredListingsForMerge.py

import pandas as pd
from config import PROCESSED_DATA_DIR

# Load raw inputs
input_file = PROCESSED_DATA_DIR / "s6_engineered_listings.csv"
df = pd.read_csv(input_file)

# Drop rows with missing key identifiers
df_cleaned = df.dropna(subset=["Listing ID", "Raw Characteristics"])

# Save cleaned version
output_file = PROCESSED_DATA_DIR / "s7aa_engineered_listings_cleaned.csv"
df_cleaned.to_csv(output_file, index=False)

print("✅ Cleaned and saved to:", output_file.name)
