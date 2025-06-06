# 🏗️ ScrapeML — Real Estate Data Pipeline

A modular Python project to scrape, clean, and analyze real estate listings from bezrealitky.com. It includes full data extraction, cleaning, feature engineering, and preparation for machine learning models.

---

## 🚀 Features

- ✅ Sitemap-based scraping (~16,000+ listings)
- ✅ Multi-stage filtering of inactive/duplicate listings
- ✅ Currency normalization (CZK, EUR)
- ✅ Feature engineering from JSON blobs
- ✅ Category & location extraction from raw titles
- ✅ Final ML-ready dataset merge

---

## 📁 Folder Overview

- `/data/raw` – raw extracted links & raw JSONs  
- `/data/processed` – cleaned, engineered datasets  
- `/scripts` – numbered scripts for pipeline steps  
- `/dictionaries` – manually created field/label aliases  
- `/tools` – field inspectors, format checkers

---

## 🧠 How to Run

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Run the pipeline (manual or orchestrated)
python scripts/1_ExtractingAllLinksToTxt.py
...
python scripts/9_MergeFinalDataset.py
