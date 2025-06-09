# s9_MergeFinalDataset.py

import pandas as pd
from config import PROCESSED_DATA_DIR

# Load cleaned listing info with restored Listing ID
enriched_path = PROCESSED_DATA_DIR / "s7a_final_cleaned_with_category_location_cleaned.csv"
enriched = pd.read_csv(enriched_path)

# Load structured features
engineered_path = PROCESSED_DATA_DIR / "s7aa_engineered_listings_cleaned.csv"
engineered = pd.read_csv(engineered_path)

# Rename conflicting 'Location' column for clarity
if "Location" in engineered.columns:
    engineered = engineered.rename(columns={"Location": "Environment Type"})

# Merge datasets on Listing ID
merged = pd.merge(enriched, engineered, on="Listing ID", how="inner")

# Define final column order
ordered_columns = [
    "Listing ID", "URL",
    "Extracted Category", "Extracted Location", "Environment Type",
    "Listing Type", "Base Price", "Discount", "Original Price",
    "Monthly Rent", "Service Charges", "Utility Charges",
    "Administrative Fee", "Refundable Deposit", "Price per unit",
    "Layout", "Floor", "Total floors", "Condition", "Age", "EPC", "Available from",
    "Usable area", "Plot space", "Plot type"
]

# Keep only columns that exist in the merged DataFrame
ordered_columns = [col for col in ordered_columns if col in merged.columns]
merged = merged[ordered_columns]

# Save final output
output_path = PROCESSED_DATA_DIR / "s8_final_merged_dataset.csv"
merged.to_csv(output_path, index=False)

print(f"✅ Final merged dataset saved → {output_path.name}")
