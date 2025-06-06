# Filtering active and inactive links
import requests
from bs4 import BeautifulSoup
import csv
import time
import random

headers = {"User-Agent": "Mozilla/5.0"}

# Phrases in English, Czech, Slovak
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

# Load filtered links (those that passed initial sitemap scrape)
with open("data/raw/filtered_links.txt", "r", encoding="utf-8") as f:
    all_links = [line.strip() for line in f.readlines()]

active_links = []
inactive_entries = []

for url in all_links:
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # Lowercase body text, title, and h1
        page_text = soup.get_text().lower()
        title_text = (soup.title.string or "").lower()
        h1_text = (soup.find("h1").get_text(strip=True) if soup.find("h1") else "").lower()

        # Detect redirect (URL changed after request)
        redirected = res.url != url

        # Determine inactive status
        is_inactive = (
            redirected or
            any(phrase in page_text for phrase in inactive_phrases) or
            any(phrase in title_text for phrase in inactive_phrases) or
            any(phrase in h1_text for phrase in inactive_phrases)
        )

        if is_inactive:
            reason = "redirected" if redirected else "phrase match"
            inactive_entries.append([url, reason])
        else:
            active_links.append(url)

        time.sleep(random.uniform(0.3, 0.6))

    except Exception as e:
        inactive_entries.append([url, f"error: {str(e)}"])

# Save active links
with open("data/raw/active_links_only.txt", "w", encoding="utf-8") as f:
    for link in active_links:
        f.write(link + "\n")

# Save log of inactive listings for re-check or debug
with open("data/raw/inactive_links_log.csv", "w", encoding="utf-8", newline="") as logf:
    writer = csv.writer(logf)
    writer.writerow(["URL", "Reason"])
    writer.writerows(inactive_entries)
