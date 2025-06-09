# src/2_scrape/s2_FilterActiveInactive_dummie.py

from config import RAW_DATA_DIR

expected_file = RAW_DATA_DIR / "s2_active_links_checked.txt"

if expected_file.exists():
    print(f"✅ [DUMMY] Skipping filtering — using existing file: {expected_file}")
else:
    print(f"❌ [DUMMY] File missing: {expected_file}")
    print("🛑 You must run the real s2 script at least once.")
