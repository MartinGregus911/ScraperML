# 🏗️ ScraperML — Real Estate Listing Extraction & Processing Pipeline

**ScraperML** is a modular data pipeline designed to:
- Scrape real estate listings
- Filter and clean scraped data
- Extract structured features
- Enrich metadata (location, category, etc.)
- Output a final clean dataset for analysis or machine learning

---

## 📂 Project Structure

```
ScraperML/
├── main.py                      # Runs full real pipeline
├── extras/
│   └── main_dummy.py           # Runs pipeline with dummy s2, s3, s3b
│
├── config.py                   # Path configuration
├── requirements.txt
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── debug/
│
├── src/
│   ├── 1_extract/
│   │   ├── s1_ExtractAllLinksToTxt.py
│   │   ├── s2_FilterActiveInactive.py
│   │   └── extras/
│   │       └── s2_FilterActiveInactive_dummie.py
│
│   ├── 2_scrape/
│   │   ├── s3_ScrapeAllDataFromLinks_restored.py
│   │   ├── s3b_ResumeScrap_restored.py
│   │   └── extras/
│   │       ├── s3_ScrapeAllDataFromLinks_dummie.py
│   │       └── s3b_ResumeScrap_dummie.py
│
│   ├── 3_filter_clean/
│   │   ├── s4_Filter2InactiveListings.py
│   │   └── s5_CleanPriceAndFinalFilter.py
│
│   ├── 4_parse_features/
│   │   ├── s6a_ParseAndValidateRawChar.py
│   │   ├── s6b_ExtractStructuredFeatures.py
│   │   └── s6c_AddListingID_viaRawCharacteristics.py
│
│   ├── 5_enrich/
│   │   ├── s7_MainExtractCategoryAndLocationFromTitle.py
│   │   ├── s7a_CleanCategoryLocationByID.py
│   │   └── s7aa_CleanEngineeredListingsByID.py
│
│   └── 6_merge/
│       └── s8_final_merged_dataset.py
│
├── mappings/
│   ├── s6Bb_field_aliases.py
│   └── s7_title_category_map.py
│
└── utils/tools/
```

---

## ⚙️ Requirements

Install all required packages using:

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Pipeline

### ▶️ Full production run

```bash
python main.py
```

### 🧪 Dev/test run with dummy scripts

```bash
python extras/main_dummy.py
```

---

## 🔁 Pipeline Step Summary

| Step | Script | Description |
|------|--------|-------------|
| `s1` | `s1_ExtractAllLinksToTxt.py` | Extract links from sitemap |
| `s2` | `s2_FilterActiveInactive.py` | Check link availability |
| `s3` | `s3_ScrapeAllDataFromLinks_restored.py` | Scrape listing content |
| `s3b` | `s3b_ResumeScrap_restored.py` | Resume missed listings |
| `s4` | `s4_Filter2InactiveListings.py` | Filter out inactive listings |
| `s5` | `s5_CleanPriceAndFinalFilter.py` | Clean and parse price fields |
| `s6a` | `s6a_ParseAndValidateRawChar.py` | Normalize raw features |
| `s6b` | `s6b_ExtractStructuredFeatures.py` | Extract structured features |
| `s6c` | `s6c_AddListingID_viaRawCharacteristics.py` | Assign consistent IDs |
| `s7` | `s7_MainExtractCategoryAndLocationFromTitle.py` | Extract category and location |
| `s7a` | `s7a_CleanCategoryLocationByID.py` | Clean and deduplicate |
| `s7aa` | `s7aa_CleanEngineeredListingsByID.py` | Finalize listing metadata |
| `s8` | `s8_final_merged_dataset.py` | Merge to one dataset |

---

## 📦 Output

The final cleaned dataset will be saved as:

```
data/processed/s8_final_merged_dataset.csv
```

---

## 🧠 Notes

- All intermediate files are stored in `data/raw/`, `data/processed/`, and `data/debug/`.
- Dummy scripts (`s2`, `s3`, `s3b`) live in their respective `extras/` folders inside each module.
- Configuration is centralized via `config.py`.
- All file paths use `pathlib` for cross-platform safety.

---

## 📄 License

MIT — Free for personal, academic, or commercial use.
