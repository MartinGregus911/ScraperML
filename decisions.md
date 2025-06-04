# 🧠 Project Decisions – Real Estate Price Estimator

This document tracks key decisions made throughout the development of the real estate price estimator project. It covers the design rationale behind scraping, cleaning, modeling, and evaluation steps.

---

## ✅ Project Goal

Build a machine learning pipeline that estimates real estate prices based on real-world listings data scraped from bezrealitky.sk.

---

## 🔍 Phase 1: Scraping Logic

### 1. Sitemap-Based Listing Discovery

**Decision:**  
Use structured sitemap or index-style listing pages to extract all URLs pointing to real estate listings.

**Rationale:**
- Avoids relying on UI pagination or client-side JS rendering
- Enables full coverage of both active and inactive listings
- Supports regular re-scanning in future

---

### 2. Scraping Full Listings

**Decision:**  
Download and parse individual listing pages to extract structured property data, including:
- Title, Location, Layout, Area, Price, Floor, Furnishing, etc.

**Rationale:**
- Listing page contains more detailed, accurate information than previews
- Fields are available in structured HTML/JS blocks
- Needed for building a clean ML dataset

---

### 3. Handling Dead Links (404 Not Found)

**Decision:**  
Listings that return a `404` error are skipped without retrying.

**Rationale:**
- Indicates a removed or invalid listing
- Not recoverable, and not usable for training
- Wasting time and requests on them adds no value

---

### 4. Handling Other Request Failures (timeouts, server errors)

**Decision:**  
Log non-404 failures (e.g., 500, connection timeout) into a file: `failed_urls.txt`.

**Rationale:**
- Retriable failures are rare but still worth tracking
- Allows later manual or batched recovery
- Keeps the scraping session stable and continuous

---

## 📦 Output Summary (So Far)

| File                        | Description                                          |
|-----------------------------|------------------------------------------------------|
| `raw_listings.csv`          | Parsed rows from individual listing pages            |
| `failed_urls.txt`           | Log of failed non-404 fetch attempts with reason     |

---

## 🛠 In Progress

- `clean_data.py` script to convert raw data into ML-ready form
- Feature schema and normalization logic
- Data modeling pipeline: EDA, training, and evaluation

---

## 📌 Next Milestone

> Design and implement data cleaning logic for selected fields such as price, area, layout, and floor — based on the target schema.

---
