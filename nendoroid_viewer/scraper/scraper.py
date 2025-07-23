"""Simple scraper for the official Nendoroid website."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dateutil import parser

BASE_URL = "https://www.goodsmile.info/en/products/category/nendoroid_series/"
OUTPUT_FILE = Path(__file__).parent / "nendoroids.json"


def fetch_description(url: str) -> str | None:
    """Fetch the product page and extract the description."""
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    if resp.status_code != 200:
        return None
    soup = BeautifulSoup(resp.text, "html.parser")
    desc_el = soup.select_one("#description, .description")
    return desc_el.get_text(" ", strip=True) if desc_el else None


def fetch_nendoroids(page: int = 1) -> list[dict]:
    """Fetch nendoroids from the given page and return a list of dicts."""
    url = f"{BASE_URL}?page={page}"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    figures = []
    for item in soup.select(".list_products > li"):
        link = item.find("a", href=True)
        if not link:
            continue
        product_url = urljoin(BASE_URL, link["href"])
        name_el = item.select_one(".p_title")
        ann_el = item.select_one(".p_announce")
        rel_el = item.select_one(".p_date")
        name = name_el.get_text(strip=True) if name_el else None
        ann_date = parser.parse(ann_el.get_text(strip=True)).date() if ann_el else None
        rel_date = parser.parse(rel_el.get_text(strip=True)).date() if rel_el else None
        images = [img["src"] for img in item.select("img") if img.get("src")]
        description = fetch_description(product_url)
        figures.append(
            {
                "product_id": link["href"].split("/")[-1].split(".")[0],
                "name": name,
                "description": description,
                "announcement_date": ann_date,
                "release_date": rel_date,
                "images": images,
                "product_url": product_url,
            }
        )
    return figures


def scrape_all(pages: int = 1) -> None:
    all_figures = []
    for p in range(1, pages + 1):
        all_figures.extend(fetch_nendoroids(p))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_figures, f, indent=2, default=str, ensure_ascii=False)

    print(f"Saved {len(all_figures)} figures to {OUTPUT_FILE}")


if __name__ == "__main__":
    scrape_all()
