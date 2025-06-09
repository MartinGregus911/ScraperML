# s5_CleanPriceAndFinalFilter.py
import pandas as pd
import numpy as np
import re
from config import PROCESSED_DATA_DIR

input_file = PROCESSED_DATA_DIR / "s4_active_cleanable_listings.csv"
output_file = PROCESSED_DATA_DIR / "s5_final_cleaned_listings.csv"
dropped_log = PROCESSED_DATA_DIR / "s5_dropped_rows_log.csv"

df = pd.read_csv(input_file)

# --- Price parsing logic ---
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

# --- Inactive listing cleaner based on zero price and weak metadata ---
def has_useful_characteristics(x):
    return isinstance(x, str) and len(x.strip()) > 10

nonzero_price_rows = df[price_columns].fillna(0).sum(axis=1) > 0
df_cleaned = df[nonzero_price_rows & df["Raw Characteristics"].apply(has_useful_characteristics)]
df_dropped = df[~(nonzero_price_rows & df["Raw Characteristics"].apply(has_useful_characteristics))]

# Save both sets
df_cleaned.to_csv(output_file, index=False)
df_dropped.to_csv(dropped_log, index=False)

print(f"✅ Final cleaned count: {len(df_cleaned)}")
print(f"🗑️ Dropped inactive or empty rows: {len(df_dropped)}")
