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

### 📄 Addition: Layered Filtering Strategy

**Date:** 2025-06-07
**Author:** Martin

---

### 🧩 Context

We employ three layers of filtering to remove inactive or unusable listings from the dataset. Each layer adds a different kind of safeguard against false positives or garbage data.

---

### ✅ Decision

1. **s2\_FilterActiveInactive.py**: Web-level validation using phrases and HTTP responses (300–400 removed).
2. **s4\_Filter2InactiveListings.py**: Content-level keyword scan of titles to catch false-positives (\~100 removed).
3. **s6b\_CorrectingFormatOfRawChar\_Parsing.py**: Deep semantic validation of data quality and field presence (6,000+ removed).

---

### 📌 Benefits

* Ensures only legitimate, rich listings survive into the core dataset
* Adds minimal compute time compared to the added quality
* Supports reproducibility of the pipeline

---

### 🧪 Verification

Filter layers were validated during multiple test runs. Manual inspection confirmed that each filter captured a distinct and important subset of invalid records.

Each layer compounds accuracy. Even if the second layer removes few, it **adds robustness** without much cost.

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

### 📄 Decision: Core data rectification via `s5_CleanPriceAndParseNumber.py`

**Date:** 2025-06-07
**Author:** Martin

---

### 🧩 Context

Despite upstream filters (`s3`, `s4`) aiming to collect only valid listings, the dataset remained noisy, inconsistent, and partially invalid:

* Incorrect currency formatting (e.g., "CZK1230000", "€9,300")
* Broken or blank numeric fields (e.g., "0.0", "-")
* Listings passing through with invalid or missing characteristics

---

### ✅ Decision

We introduced and emphasized `s5_CleanPriceAndParseNumber.py` as the **central cleanup layer** in the scraping pipeline. Its main responsibilities:

* Normalize and convert price formats across currencies (CZK, EUR, etc.)
* Drop rows with no meaningful pricing
* Discard listings missing essential field characteristics

The impact was enormous: from \~32,000 entries, only \~9,500 passed — indicating that over **22,000 rows were silently broken or unusable** until this step enforced strong quality control.

---

### 📌 Benefits

* Strong sanity filtering
* Central logic for data consistency
* Clean numeric fields for ML, DB, or analytics
* Prevents future data rot or silent errors

---

### 🔁 Next Steps

* This step is now **non-optional** in the production pipeline
* Downstream scripts (e.g., feature extraction, ML processing) depend entirely on `s5`-cleaned output
* Deduplication may be added here for further hardening
