import pandas as pd

# Load cleaned listing info with restored Listing ID
enriched = pd.read_csv("/data/processed/final_cleaned_with_category_location_cleaned.csv")

# Load structured features
engineered = pd.read_csv("/data/processed/engineered_listings_cleaned.csv")

# Rename conflicting 'Location' column for clarity
if "Location" in engineered.columns:
    engineered = engineered.rename(columns={"Location": "Environment Type"})

# Merge datasets on Listing ID
merged = pd.merge(enriched, engineered, on="Listing ID", how="inner")

# Final column order
ordered_columns = [
    "Listing ID", "URL",
    "Extracted Category", "Extracted Location", "Environment Type",
    "Listing Type", "Base Price", "Discount", "Original Price",
    "Monthly Rent", "Service Charges", "Utility Charges",
    "Administrative Fee", "Refundable Deposit", "Price per unit",
    "Layout", "Floor", "Total floors", "Condition", "Age", "EPC", "Available from",
    "Usable area", "Plot space", "Plot type"
]

# Keep only columns that exist
ordered_columns = [col for col in ordered_columns if col in merged.columns]
merged = merged[ordered_columns]

# Save output
merged.to_csv("/data/processed/final_merged_dataset.csv", index=False)
print("✅ Final merged dataset saved as final_merged_dataset.csv")
