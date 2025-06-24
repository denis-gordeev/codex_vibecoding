"""Simple scraper for the official Nendoroid website."""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import json

BASE_URL = "https://www.goodsmile.info/en/products/category/nendoroid_series/"
OUTPUT_FILE = Path(__file__).parent / "nendoroids.json"


def fetch_nendoroids(page: int = 1) -> list[dict]:
    """Fetch nendoroids from the given page and return a list of dicts."""
    url = f"{BASE_URL}?page={page}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    figures = []
    for item in soup.select(".list_products > li"):  # CSS selectors depend on site
        name_el = item.select_one(".p_title")
        date_el = item.select_one(".p_date")
        if not name_el:
            continue
        name = name_el.text.strip()
        release_date = date_el.text.strip() if date_el else None
        figures.append({
            "name": name,
            "release_date": release_date,
        })
    return figures


def scrape_all(pages: int = 1):
    all_figures = []
    for p in range(1, pages + 1):
        all_figures.extend(fetch_nendoroids(p))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_figures, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(all_figures)} figures to {OUTPUT_FILE}")


if __name__ == "__main__":
    scrape_all()
