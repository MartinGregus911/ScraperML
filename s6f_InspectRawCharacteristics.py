
import pandas as pd

# Load the cleaned final listings
df = pd.read_csv("final_cleaned_listings.csv")

# Extract a sample of 10 Raw Characteristics for inspection
sample = df["Raw Characteristics"].dropna().sample(10, random_state=42)

# Save to CSV for review
sample.to_csv("raw_characteristics_sample.csv", index=False)
print("✅ Saved sample to raw_characteristics_sample.csv")
