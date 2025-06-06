import pandas as pd

# Load enriched data with category/location
df = pd.read_csv("final_cleaned_with_category_location.csv")

# Keep only rows with a non-null Listing ID
df_cleaned = df[df["Listing ID"].notna()]

# Save result
df_cleaned.to_csv("final_cleaned_with_category_location_cleaned.csv", index=False)

print(f"✅ Cleaned: {len(df_cleaned)} rows saved to final_cleaned_with_category_location_cleaned.csv")
