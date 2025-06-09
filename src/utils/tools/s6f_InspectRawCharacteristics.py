# s6C_SampleRawCharacteristics.py

import pandas as pd
from config import PROCESSED_DATA_DIR, RAW_DATA_DIR

# Load the cleaned final listings
input_file = PROCESSED_DATA_DIR / "s5_final_cleaned_listings.csv"
df = pd.read_csv(input_file)

# Extract a sample of 10 Raw Characteristics for inspection
sample = df["Raw Characteristics"].dropna().sample(10, random_state=42)

# Save to CSV for review
output_file = RAW_DATA_DIR / "s6f_raw_characteristics_sample.csv"
sample.to_csv(output_file, index=False)

print(f"✅ Saved sample to {output_file.name}")
