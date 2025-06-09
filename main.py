# main.py — clean, strict, and reliable full pipeline runner

import sys
from subprocess import run
from time import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Ordered pipeline scripts — real filenames only
scripts = [
    ("s1", BASE_DIR / "src" / "1_extract" / "s1_ExtractAllLinksToTxt.py"),
    ("s2", BASE_DIR / "src" / "1_extract" / "s2_FilterActiveInactive.py"),
    ("s3", BASE_DIR / "src" / "2_scrape" / "s3_ScrapeAllDataFromLinks_restored.py"),
    ("s3b", BASE_DIR / "src" / "2_scrape" / "s3b_ResumeScrap_restored.py"),
    ("s4", BASE_DIR / "src" / "3_filter_clean" / "s4_Filter2InactiveListings.py"),
    ("s5", BASE_DIR / "src" / "3_filter_clean" / "s5_CleanPriceAndFinalFilter.py"),
    ("s6a", BASE_DIR / "src" / "4_parse_features" / "s6a_ParseAndValidateRawChar.py"),
    ("s6b", BASE_DIR / "src" / "4_parse_features" / "s6b_ExtractStructuredFeatures.py"),
    ("s6c", BASE_DIR / "src" / "4_parse_features" / "s6c_AddListingID_viaRawCharacteristics.py"),
    ("s7", BASE_DIR / "src" / "5_enrich" / "s7_MainExtractCategoryAndLocationFromTitle.py"),
    ("s7a", BASE_DIR / "src" / "5_enrich" / "s7a_CleanCategoryLocationByID.py"),
    ("s7aa", BASE_DIR / "src" / "5_enrich" / "s7aa_CleanEngineeredListingsByID.py"),
    ("s8", BASE_DIR / "src" / "6_merge" / "s8_final_merged_dataset.py"),
]


def run_script(step_name, script_path: Path):
    print(f"\n▶️ [{step_name}] Running: {script_path}")

    if not script_path.exists():
        print(f"❌ [{step_name}] File not found: {script_path}")
        sys.exit(1)

    start = time()
    result = run([sys.executable, str(script_path)])
    elapsed = time() - start

    if result.returncode == 0:
        print(f"✅ [{step_name}] Done in {elapsed:.1f} sec")
    else:
        print(f"❌ [{step_name}] Failed — Exit code: {result.returncode}")
        sys.exit(result.returncode)


if __name__ == "__main__":
    print("🚀 Starting pipeline...\n")
    for step, path in scripts:
        run_script(step, path)
    print("\n🎉 All steps completed successfully.")
