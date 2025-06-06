import pandas as pd

df = pd.read_csv("/data/processed/cleaned_listings.csv")
df_filtered = df[~df["Title"].str.contains("no longer active", case=False, na=False)]
df_filtered.to_csv("final_cleaned_listings.csv", index=False)

print(f"Triple filtering complete. Final cleaned listings saved to final_cleaned_listings.csv")
print(f"Dropped {len(df) - len(df_filtered)} additional listings.")
