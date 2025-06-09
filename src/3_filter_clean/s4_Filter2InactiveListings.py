# s4_Filter2InactiveListings.py

import sys
from pathlib import Path
import pandas as pd

# Ensure the project root (where config.py lives) is in the import path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR

# I/O paths
input_path = RAW_DATA_DIR / "s3_active_listings_with_prices_and_features.csv"
output_path = PROCESSED_DATA_DIR / "s4_active_cleanable_listings.csv"

# Load scraped data
df = pd.read_csv(input_path)
initial_count = len(df)

# Define inactive marker phrases
inactive_phrases = [
    "no longer active",
    "this property is not available",
    "inzerát již není v nabídce",
    "inzerát už nie je v ponuke",
    "táto ponuka už nie je aktuálna",
    "nabídka již není aktuální",
    "tento inzerát již neexistuje",
    "tento inzerát už neexistuje"
]

# Filter out rows with inactive indicators in the Title
inactive_mask = df["Title"].str.lower().fillna("").apply(
    lambda title: any(phrase in title for phrase in inactive_phrases)
)

df_filtered = df[~inactive_mask].copy()
df_dropped = df[inactive_mask].copy()
dropped_count = len(df_dropped)

# Save filtered output
df_filtered.to_csv(output_path, index=False)

# Print summary
print(f"🔍 Initial listings: {initial_count}")
print(f"🗑️ Inactive removed: {dropped_count}")
print(f"✅ Remaining active: {len(df_filtered)}")
print(f"📄 Output saved to: {output_path}")
