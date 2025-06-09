### 📄 Decision: Normalize project-wide path structure

**Date:** 2025-06-05
**Author:** Martin

---

### 🧩 Context

Across this ScraperML project, path handling in scripts was inconsistent. We observed the following:

* Scripts using relative string paths (e.g., "data/raw/xyz.csv")
* Others using `Path(__file__).resolve().parent.parent`
* Yet others using custom variables like `ROOT` or `BASE_DIR`

This inconsistency led to difficulties in maintaining and refactoring the project when folder structure changed or when individual scripts were run in isolation.

---

### ✅ Decision

We introduced a consistent centralized pattern for defining and importing paths across the whole project. This is implemented via a shared `config.py` module at the root level.

```python
# config.py
from pathlib import Path
ROOT = Path(__file__).resolve().parent
RAW_DATA_DIR = ROOT / "data" / "raw"
PROCESSED_DATA_DIR = ROOT / "data" / "processed"
DEBUG_DIR = ROOT / "data" / "debug"
```

Each script imports these constants instead of hardcoding their own logic:

```python
from config import RAW_DATA_DIR
input_file = RAW_DATA_DIR / "active_links_only.txt"
```

---

### 📌 Benefits

* Easier to restructure folder layout
* Reduces risk of path mismatch bugs
* Easier onboarding for new contributors
* Encourages modular script design

---

### 🧪 Verification

Tested on Windows using PyCharm with `.venv`, verified working across:

* Relative script runs
* Top-down project execution
* Path creation for new folders/files

---

### 🔁 Next Steps

We plan to apply this principle retroactively across all existing scripts (s1–s9) and enforce it for any new development in this repository.

---

### 📄 Addition: Resume Scraping Mode

**Date:** 2025-06-06
**Author:** Martin

---

### 🧩 Context

Scraping a large dataset (\~16k listings) risks interruption from network errors, rate limits, or crashes. Restarting the entire scrape would be inefficient.

---

### ✅ Decision

We added a `ResumeScrapingIfInterrupted.py` script that:

* Loads previously scraped URLs from the output file
* Compares them to `active_links_only.txt`
* Scrapes only URLs that haven't been processed yet

This prevents duplication and allows resuming long-running scraping sessions reliably.

---

### 📌 Benefits

* Saves time and avoids rescraping existing data
* Supports crash recovery
* Enables flexible chunk-based scraping or throttled batch runs

---

### 🔁 Usage Example

```bash
python s3b_ResumeScrapingIfInterrupted.py
```

Output appends directly to the same output file as `s3`, ensuring a seamless dataset accumulation.

---

### 🔁 Future Step

We may consider integrating this logic directly into the core `s3` script with a `--resume` CLI flag for a unified scraping interface.

---

### 📦 Project Workflow Tree (Updated 2025-06-07)

```
  ┌────────────────────────────┐
  │  Sitemaps (bezrealitky.com)│
  └────────────┬───────────────┘
               │
               ▼
  s1_ExtractAllLinksToTxt.py
  Output: all_listing_links.txt

    ▼
  s2_FilterActiveInactive.py
  Output:
    - active_links_only.txt
    - inactive_links_log.csv

    ▼
  s3_ScrapeAllDataFromLinks.py
  Output: active_listings_with_prices_and_features.csv

    ├── s3b_ResumeScrap.py (optional resume)
    ▼
  s4_Filter2InactiveListings.py
  Output: active_cleanable_listings.csv

    ▼
  s5_CleanPriceAndParseNumber.py
  Output:
    - cleaned_listings.csv
    - dropped_rows_log.csv

    ▼
  s6z_ParseRawCharAndRestoreID.py
  Output: final_cleaned_listings.csv

    ▼
  s6_MainFeatureEngineering.py
  Output: engineered_listings.csv

    ├── s6a_ScanRawCharacteristicHealth.py
    ├── s6A_SearchingForFaultyFormattingOfRawChar.py
    ├── s6b_CorrectingFormatOfRawChar_Parsing.py
    ├── s6B_FieldNameFrequencies.py
    ├── s6Bb_field_aliases.py
    ├── s6f_InspectRawCharacteristics.py

    ▼
  s7_MainExtractCategoryAndLocationFromTitle.py
  Output: final_cleaned_with_category_location.csv

    ├── s7a_CleanCategoryLocationByID.py
    ├── s7aa_CleanEngineeredListingsByID.py

    ▼
  s8_final_merged_dataset.py
  Output: final_merged_dataset.csv
```

Each branch includes its output and inner support scripts, kept modular and processed via consistent path structures defined in `config.py`.
