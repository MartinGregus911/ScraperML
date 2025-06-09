# src/2_scrape/s3_ScrapeAllDataFromLinks_dummie.py

from config import RAW_DATA_DIR

expected_file = RAW_DATA_DIR / "s3_active_listings_with_prices_and_features.csv"

if expected_file.exists():
    print(f"✅ [DUMMY] Skipping scrape — using existing file: {expected_file}")
else:
    print(f"❌ [DUMMY] File missing: {expected_file}")
    print("🛑 You must run the real s3 scraper at least once.")
