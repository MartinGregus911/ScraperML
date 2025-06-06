import pandas as pd

# Load the full scraped dataset
input_file = "data/raw/active_listings_with_prices_and_features.csv"
output_file = "data/processed/active_cleanable_listings.csv"

# Read the CSV
df = pd.read_csv(input_file)

# Identify rows that say the listing is no longer active
inactive_mask = df["Title"].str.contains("no longer active", case=False, na=False)

# Report how many were removed
removed_count = inactive_mask.sum()
print(f"🧹 Removed {removed_count} inactive listings.")

# Keep only active listings
df_cleanable = df[~inactive_mask].copy()

# Save to new output file
df_cleanable.to_csv(output_file, index=False)
print(f"✅ Filtered data saved to: {output_file}")
