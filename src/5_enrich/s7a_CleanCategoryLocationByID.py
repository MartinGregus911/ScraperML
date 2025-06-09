# s7z_CleanupCategoryLocationListingID.py

import pandas as pd
from config import PROCESSED_DATA_DIR

# Load enriched data with category/location
input_file = PROCESSED_DATA_DIR / "s7_final_cleaned_with_category_location.csv"
df = pd.read_csv(input_file)

# Keep only rows with a non-null Listing ID
df_cleaned = df[df["Listing ID"].notna()]

# Save result
output_file = PROCESSED_DATA_DIR / "s7a_final_cleaned_with_category_location_cleaned.csv"
df_cleaned.to_csv(output_file, index=False)

print(f"✅ Cleaned: {len(df_cleaned)} rows saved to {output_file.name}")
