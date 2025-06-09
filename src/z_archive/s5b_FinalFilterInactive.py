# s5b_FinalFilterInactive.py
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"

input_file = PROCESSED / "cleaned_listings.csv"
output_file = ROOT / "final_cleaned_listings.csv"

df = pd.read_csv(input_file)
initial_count = len(df)
inactive_mask = df["Title"].str.contains("no longer active", case=False, na=False)
df_filtered = df[~inactive_mask].copy()

df_filtered.to_csv(output_file, index=False)
print(f"🚫 Final filter removed {inactive_mask.sum()} more inactive listings.")
print(f"✅ Final cleaned dataset saved to {output_file} (Count: {len(df_filtered)})")
