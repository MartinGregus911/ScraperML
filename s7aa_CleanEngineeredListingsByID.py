import pandas as pd

# Load raw inputs
engineered = pd.read_csv("engineered_listings.csv")


# Drop rows with missing key identifiers
engineered_clean = engineered.dropna(subset=["Listing ID", "Raw Characteristics"])


# Save cleaned versions
engineered_clean.to_csv("engineered_listings_cleaned.csv", index=False)


print("✅ Cleaned and saved for Step 9 merge input.")
