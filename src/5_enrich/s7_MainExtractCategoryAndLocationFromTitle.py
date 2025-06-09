# s7_MainExtractCategoryAndLocationFromTitle.py

import re
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from config import PROCESSED_DATA_DIR
from src.utils.mappings.s7_title_category_map import title_category_map

input_file = PROCESSED_DATA_DIR / "s6z_final_cleaned_with_id.csv"
output_file = PROCESSED_DATA_DIR / "s7_final_cleaned_with_category_location.csv"

df = pd.read_csv(input_file)

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

def clean_title(title):
    title = str(title)
    for noise in noise_patterns:
        title = title.replace(noise, "")
    for layout in layout_patterns:
        title = re.sub(re.escape(layout), "", title, flags=re.IGNORECASE)
    title = re.sub(r"\d+\s?(m²|m2)", "", title)
    return title.strip()

def extract_category(title):
    cleaned = clean_title(title)
    for phrase, normalized in title_category_map.items():
        if phrase.lower() in cleaned.lower():
            return normalized
    return "Unknown"

def extract_location(title):
    cleaned = clean_title(title)
    for alias in title_category_map.keys():
        cleaned = re.sub(re.escape(alias), "", cleaned, flags=re.IGNORECASE)
    match = re.search(r"[,•]*\s*(.+)$", cleaned)
    return match.group(1).strip() if match else ""

df["Extracted Category"] = df["Title"].apply(extract_category)
df["Extracted Location"] = df["Title"].apply(extract_location)

df.to_csv(output_file, index=False)
print(f"✅ Output saved as {output_file.name}")
