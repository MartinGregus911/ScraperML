# s2_FilterActiveInactive.py

import csv
import random
import time
import requests
from bs4 import BeautifulSoup
from config import RAW_DATA_DIR

headers = {"User-Agent": "Mozilla/5.0"}

# Clear I/O structure
input_links_path = RAW_DATA_DIR / "s1_all_listing_links.txt"
active_output_path = RAW_DATA_DIR / "s2_active_links_checked.txt"
inactive_output_log = RAW_DATA_DIR / "s2_inactive_links_log.csv"
failed_output_log = RAW_DATA_DIR / "s2_failed_links_log.csv"

inactive_phrases = [
    "this listing is no longer active",
    "this property is not available",
    "inzerát již není v nabídce",
    "inzerát už nie je v ponuke",
    "táto ponuka už nie je aktuálna",
    "nabídka již není aktuální",
    "tento inzerát již neexistuje",
    "tento inzerát už neexistuje"
]

active_links = []
inactive_entries = []
failed_entries = []

with open(input_links_path, "r", encoding="utf-8") as f:
    all_links = [line.strip() for line in f.readlines() if line.strip()]

total_links = len(all_links)

for idx, url in enumerate(all_links, start=1):
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        text_combined = " ".join([
            soup.get_text().lower(),
            (soup.title.string or "").lower(),
            (soup.find("h1").get_text(strip=True) if soup.find("h1") else "").lower()
        ])
        redirected = res.url != url
        is_inactive = redirected or any(p in text_combined for p in inactive_phrases)

        if is_inactive:
            reason = "redirected" if redirected else "phrase match"
            inactive_entries.append([url, reason])
            print(f"[{idx:05}/{total_links}] 🗑️ Inactive ({reason}): {url}")
        else:
            active_links.append(url)
            print(f"[{idx:05}/{total_links}] ✅ Active: {url}")

        time.sleep(random.uniform(0.3, 0.6))

    except Exception as e:
        failed_entries.append([url, str(e)])
        print(f"[{idx:05}/{total_links}] ⚠️ Failed: {url} — {e}")

# Save results
with open(active_output_path, "w", encoding="utf-8") as f:
    f.writelines(link + "\n" for link in active_links)

with open(inactive_output_log, "w", encoding="utf-8", newline="") as logf:
    writer = csv.writer(logf)
    writer.writerow(["URL", "Reason"])
    writer.writerows(inactive_entries)

with open(failed_output_log, "w", encoding="utf-8", newline="") as logf:
    writer = csv.writer(logf)
    writer.writerow(["URL", "Error"])
    writer.writerows(failed_entries)

# Final summary
print(f"\n✅ Active: {len(active_links)}")
print(f"🗑️ Inactive: {len(inactive_entries)}")
print(f"⚠️ Failed: {len(failed_entries)}")
print(f"📦 Total checked: {total_links}")
