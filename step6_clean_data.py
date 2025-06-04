import pandas as pd
import numpy as np
import re

df = pd.read_csv("active_listings_with_prices_and_features.csv")

def parse_and_convert_price(value):
    if pd.isna(value):
        return np.nan
    value = str(value).replace("\u00A0", "").replace(",", "").strip()
    if not re.search(r"\d", value):
        return np.nan
    if "€" in value or "EUR" in value:
        numeric = re.sub(r"[^\d.]", "", value)
        try:
            return float(numeric) * 25.5
        except ValueError:
            return np.nan
    if "CZK" in value.upper() or value.upper().startswith("CZK"):
        numeric = re.sub(r"[^\d]", "", value)
        try:
            return float(numeric)
        except ValueError:
            return np.nan
    try:
        return float(value)
    except ValueError:
        return np.nan

price_columns = [
    "Base Price", "Discount", "Original Price", "Monthly Rent",
    "Service Charges", "Utility Charges", "Administrative Fee", "Refundable Deposit"
]

for col in price_columns:
    df[col] = df[col].apply(parse_and_convert_price)

def has_useful_characteristics(x):
    return isinstance(x, str) and len(x.strip()) > 10

nonzero_price_rows = df[price_columns].fillna(0).sum(axis=1) > 0
df_cleaned = df[nonzero_price_rows & df["Raw Characteristics"].apply(has_useful_characteristics)]
df_dropped = df[~(nonzero_price_rows & df["Raw Characteristics"].apply(has_useful_characteristics))]

df_cleaned.to_csv("cleaned_listings.csv", index=False)
df_dropped.to_csv("dropped_rows_log.csv", index=False)

print("✅ Cleaned listings saved to cleaned_listings.csv")
print("🗑️ Dropped rows saved to dropped_rows_log.csv")
print(f"✔️ Final cleaned count: {len(df_cleaned)} | Dropped: {len(df_dropped)}")