import pandas as pd
import re
from s7_title_category_map import title_category_map

# Load dataset
df = pd.read_csv("/data/processed/final_cleaned_with_id.csv")

# Common cleanup terms
noise_patterns = [
    "without real estate", "bez realitky", "bez realitnej kancelárie"
]

layout_patterns = [
    "1 bedroom", "1+1", "1+kk",
    "2 bedroom", "2+1", "2+kk",
    "3+1", "3+kk",
    "4+1", "4+kk",
    "5 bedroom", "5+1", "5+kk",
    "6+1", "6+kk",
    "7+1", "7+kk",
    "Garsoniéra", "Small studio", "Studio"
]


# Normalize layout-like noise before extracting anything
def clean_title(title):
    title = str(title)
    for noise in noise_patterns:
        title = title.replace(noise, "")
    for layout in layout_patterns:
        title = re.sub(re.escape(layout), "", title, flags=re.IGNORECASE)
    title = re.sub(r"\d+\s?(m²|m2)", "", title)  # remove area
    return title.strip()

# Extract category from cleaned title
def extract_category(title):
    cleaned = clean_title(title)
    for phrase, normalized in title_category_map.items():
        if phrase.lower() in cleaned.lower():
            return normalized
    return "Unknown"

# Extract location from cleaned title
def extract_location(title):
    cleaned = clean_title(title)
    for alias in title_category_map.keys():
        cleaned = re.sub(re.escape(alias), "", cleaned, flags=re.IGNORECASE)
    match = re.search(r"[,•]*\s*(.+)$", cleaned)
    return match.group(1).strip() if match else ""

# Apply
df["Extracted Category"] = df["Title"].apply(extract_category)
df["Extracted Location"] = df["Title"].apply(extract_location)

# Save result
df.to_csv("/data/processed/final_cleaned_with_category_location.csv", index=False)
print("✅ Output saved as final_cleaned_with_category_location.csv")
