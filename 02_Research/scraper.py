"""
2B Oil Business — Groundnut Oil Market Research Scraper
========================================================
Scrapes brand websites and marketplaces for cold-pressed groundnut oil data.
Outputs:
  - D:/Cold-Pressed Oil Business/02_Research/scraped_data.csv
  - Appends findings to D:/Cold-Pressed Oil Business/02_Research/Competitor_Research.md

Usage:
  python scraper.py

Sources covered:
  - Brand websites: Wood Press, Anveshan, Marachekku, Two Brothers, Gramiyum,
                    Conscious Food, Jivika Naturals, Praakritik, Nutriorg
  - Amazon.in search results
  - BigBasket search results
  - Flipkart search results (limited - JS heavy)
"""

import asyncio
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# ── Config ────────────────────────────────────────────────────────────────────
OUTPUT_DIR   = Path("D:/Cold-Pressed Oil Business/02_Research")
CSV_OUT      = OUTPUT_DIR / "scraped_data.csv"
MD_OUT       = OUTPUT_DIR / "Competitor_Research.md"
TODAY        = date.today().isoformat()
TIMEOUT      = 20_000   # ms per page
HEADLESS     = True

# ── Structured target list ────────────────────────────────────────────────────
# Each entry: (seller_name, seller_type, url, scrape_strategy, is_hyderabad)
TARGETS = [
    # Brand websites
    ("Wood Press",          "Brand – own website", "https://woodpressedoil.com/product-category/groundnut-oil/",        "generic", False),
    ("Anveshan",            "Brand – own website", "https://anveshan.farm/collections/groundnut-oil",                   "generic", False),
    ("Marachekku",          "Brand – own website", "https://www.marachekku.com/collections/all",                        "generic", False),
    ("Two Brothers Organic","Brand – own website", "https://twobrothersindiashop.com/collections/groundnut-oil",        "generic", False),
    ("Gramiyum",            "Brand – own website", "https://www.gramiyum.in/product-category/oils/",                    "generic", False),
    ("Conscious Food",      "Brand – own website", "https://www.consciousfood.com/product-category/oils/",              "generic", False),
    ("Jivika Naturals",     "Brand – own website", "https://www.jivikaorganics.com/product-category/cold-pressed-oils/","generic", False),
    ("Praakritik",          "Brand – own website", "https://www.praakritik.com/collections/oils",                       "generic", False),
    ("Nutriorg",            "Brand – own website", "https://www.nutriorg.com/collections/oils",                         "generic", False),
    ("Pure & Sure",         "Brand – own website", "https://pureandsurenow.com/product-category/oils/",                 "generic", False),
    ("Sri Sri Tattva",      "Brand – own website", "https://www.srisritattva.com/collections/oils",                     "generic", False),
    # Marketplaces
    ("Amazon.in",           "Marketplace",         "https://www.amazon.in/s?k=cold+pressed+groundnut+oil+1+litre&rh=n%3A1351118031", "amazon", False),
    ("BigBasket",           "Marketplace",         "https://www.bigbasket.com/ps/?q=cold+pressed+groundnut+oil&nc=as",  "generic", False),
    ("Flipkart",            "Marketplace",         "https://www.flipkart.com/search?q=cold+pressed+groundnut+oil+1+litre", "generic", False),
]

PROCESS_TERMS = [
    "cold-pressed", "cold pressed", "wood pressed", "wood-pressed",
    "kachi ghani", "chekku", "ganuga", "wooden ghani", "expeller"
]

VARIETY_TERMS = ["java", "bold", "tac", "virginia", "k6", "tmv"]

CSV_FIELDS = [
    "seller_name", "seller_type", "product_name", "pack_size_ml",
    "listed_price_inr", "price_per_litre_inr", "delivery_fee",
    "process_claim", "variety_claim", "packaging_type",
    "rating", "review_count", "channels", "is_hyderabad",
    "source_url", "retrieved_date", "confidence", "limitations", "raw_notes"
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_price(text: str) -> float | None:
    """Pull first ₹ price from a string."""
    text = text.replace(",", "")
    m = re.search(r"[₹\u20b9Rs\.]*\s*(\d+(?:\.\d+)?)", text)
    return float(m.group(1)) if m else None

def price_per_litre(price: float | None, pack_ml: int | None) -> float | None:
    if price and pack_ml and pack_ml > 0:
        return round(price / (pack_ml / 1000), 2)
    return None

def detect_process(text: str) -> str:
    text_lower = text.lower()
    found = [t for t in PROCESS_TERMS if t in text_lower]
    return "; ".join(found) if found else "—"

def detect_variety(text: str) -> str:
    text_lower = text.lower()
    found = [t for t in VARIETY_TERMS if t in text_lower]
    return "; ".join(found) if found else "—"

def detect_packaging(text: str) -> str:
    text_lower = text.lower()
    types = []
    if "glass" in text_lower: types.append("glass")
    if "plastic" in text_lower or "hdpe" in text_lower or "pet" in text_lower: types.append("plastic")
    if "steel" in text_lower or "tin" in text_lower: types.append("steel/tin")
    if "pouch" in text_lower or "sachet" in text_lower: types.append("pouch")
    return "; ".join(types) if types else "—"

def extract_pack_ml(text: str) -> int | None:
    """Extract pack size in ml from product name/title."""
    text = text.lower()
    # litre patterns first
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:litre|ltr|liter|l)\b", text)
    if m:
        return int(float(m.group(1)) * 1000)
    # ml patterns
    m = re.search(r"(\d+)\s*(?:ml|millilitre)", text)
    if m:
        return int(m.group(1))
    # standalone number after x or comma that looks like 500, 1000
    m = re.search(r"\b(250|500|750|1000|1500|2000|3000|5000)\b", text)
    if m:
        return int(m.group(1))
    return None

# ── Scrape strategies ─────────────────────────────────────────────────────────

async def scrape_generic(page, url: str, seller_name: str, seller_type: str, is_hyd: bool) -> list[dict]:
    """Generic scraper — works for most brand websites and BigBasket."""
    results = []
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=TIMEOUT)
        await page.wait_for_timeout(2000)
        html = await page.content()
    except PlaywrightTimeout:
        return [_error_row(seller_name, seller_type, url, is_hyd, "Timeout loading page")]

    soup = BeautifulSoup(html, "lxml")
    page_text = soup.get_text(" ", strip=True)

    # Try to find product cards / items
    # Common selectors across Shopify, WooCommerce, custom sites
    product_blocks = (
        soup.select(".product-item, .product-card, .woocommerce-LoopProduct, "
                    ".product_item, li.product, .grid__item, .boost-pfs-filter-product-item, "
                    ".product-list-item, [data-product-id], .s-result-item")
    )

    if not product_blocks:
        # Fallback: scrape the whole page text for price + product signals
        row = _build_row(
            seller_name, seller_type, "—", None, None, None, "—",
            detect_process(page_text), detect_variety(page_text),
            detect_packaging(page_text), None, None,
            seller_name, is_hyd, url, TODAY,
            "Low – full page fallback, no product cards found",
            "Could not isolate individual product cards", page_text[:300]
        )
        return [row]

    for block in product_blocks[:10]:   # cap at 10 per page
        block_text = block.get_text(" ", strip=True)

        # Product name
        name_el = block.select_one("h2, h3, h1, .product-title, .woocommerce-loop-product__title, "
                                   ".product-name, [class*='title'], [class*='name']")
        product_name = name_el.get_text(strip=True) if name_el else block_text[:80]

        # Only keep groundnut / peanut products
        if not any(w in product_name.lower() for w in ["groundnut", "peanut", "moongphali", "pallilu"]):
            continue

        # Price
        price_el = block.select_one(".price, .woocommerce-Price-amount, [class*='price'], "
                                    "span.amount, .product-price, .Price")
        price_text = price_el.get_text(strip=True) if price_el else ""
        listed_price = extract_price(price_text)

        # Pack size from name
        pack_ml = extract_pack_ml(product_name)

        row = _build_row(
            seller_name, seller_type, product_name, pack_ml,
            listed_price, price_per_litre(listed_price, pack_ml),
            "—",
            detect_process(block_text + " " + page_text[:500]),
            detect_variety(block_text),
            detect_packaging(block_text),
            None, None,
            seller_name, is_hyd, url, TODAY,
            "Medium – product card found, price may need verification",
            "Rating/reviews not captured; delivery fee not captured",
            block_text[:200]
        )
        results.append(row)

    return results if results else [_error_row(seller_name, seller_type, url, is_hyd,
                                               "No groundnut products found on page")]

async def scrape_amazon(page, url: str) -> list[dict]:
    """Amazon.in search results scraper."""
    results = []
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=TIMEOUT)
        await page.wait_for_timeout(3000)
        html = await page.content()
    except PlaywrightTimeout:
        return [_error_row("Amazon.in", "Marketplace", url, False, "Timeout loading Amazon search")]

    soup = BeautifulSoup(html, "lxml")

    items = soup.select("[data-component-type='s-search-result']")
    if not items:
        items = soup.select(".s-result-item[data-asin]")

    for item in items[:15]:
        asin = item.get("data-asin", "")
        if not asin:
            continue

        # Product title
        title_el = item.select_one("h2 a span, .a-size-medium, .a-size-base-plus")
        title = title_el.get_text(strip=True) if title_el else "—"

        if not any(w in title.lower() for w in ["groundnut", "peanut", "moongphali"]):
            continue

        # Price
        price_el = item.select_one(".a-price .a-offscreen, .a-price-whole")
        price_text = price_el.get_text(strip=True) if price_el else ""
        listed_price = extract_price(price_text)

        # Rating
        rating_el = item.select_one(".a-icon-alt")
        rating_text = rating_el.get_text(strip=True) if rating_el else ""
        rating_m = re.search(r"(\d+\.\d+)", rating_text)
        rating = float(rating_m.group(1)) if rating_m else None

        # Review count
        review_el = item.select_one(".a-size-small .a-link-normal")
        review_text = review_el.get_text(strip=True).replace(",", "") if review_el else ""
        review_m = re.search(r"(\d+)", review_text)
        review_count = int(review_m.group(1)) if review_m else None

        # Seller name from listing
        seller_el = item.select_one(".a-size-small.a-color-secondary")
        seller_name = seller_el.get_text(strip=True) if seller_el else "Amazon marketplace seller"
        seller_name = re.sub(r"^by\s+", "", seller_name, flags=re.I).strip() or "Amazon marketplace seller"

        pack_ml = extract_pack_ml(title)
        item_text = item.get_text(" ", strip=True)
        product_url = f"https://www.amazon.in/dp/{asin}"

        row = _build_row(
            seller_name, "Marketplace – Amazon.in", title, pack_ml,
            listed_price, price_per_litre(listed_price, pack_ml),
            "—",
            detect_process(item_text),
            detect_variety(item_text),
            detect_packaging(item_text),
            rating, review_count,
            "Amazon.in", False,
            product_url, TODAY,
            "Medium – search result card; price may differ on product page",
            "Seller type unverified; delivery fee not captured; rating is search-result snippet",
            title[:200]
        )
        results.append(row)

    return results if results else [_error_row("Amazon.in", "Marketplace", url, False,
                                               "No groundnut results parsed from Amazon search")]

# ── Row builders ──────────────────────────────────────────────────────────────

def _build_row(seller_name, seller_type, product_name, pack_ml, listed_price,
               ppl, delivery_fee, process_claim, variety_claim, packaging_type,
               rating, review_count, channels, is_hyd, source_url, retrieved,
               confidence, limitations, raw_notes) -> dict:
    return {
        "seller_name":         seller_name,
        "seller_type":         seller_type,
        "product_name":        product_name,
        "pack_size_ml":        pack_ml if pack_ml else "—",
        "listed_price_inr":    listed_price if listed_price else "—",
        "price_per_litre_inr": ppl if ppl else "—",
        "delivery_fee":        delivery_fee,
        "process_claim":       process_claim,
        "variety_claim":       variety_claim,
        "packaging_type":      packaging_type,
        "rating":              rating if rating else "—",
        "review_count":        review_count if review_count else "—",
        "channels":            channels,
        "is_hyderabad":        "Yes" if is_hyd else "No",
        "source_url":          source_url,
        "retrieved_date":      retrieved,
        "confidence":          confidence,
        "limitations":         limitations,
        "raw_notes":           raw_notes,
    }

def _error_row(seller_name, seller_type, url, is_hyd, reason) -> dict:
    return _build_row(
        seller_name, seller_type, "—", None, None, None, "—",
        "—", "—", "—", None, None, seller_name, is_hyd, url, TODAY,
        "None – page inaccessible", reason, ""
    )

# ── Markdown writer ───────────────────────────────────────────────────────────

def rows_to_markdown(rows: list[dict]) -> str:
    valid = [r for r in rows if r["listed_price_inr"] != "—"]
    errors = [r for r in rows if r["listed_price_inr"] == "—"]

    lines = [
        f"# 2B — All-India Competitor Research",
        f"",
        f"**Status:** Scraped  ",
        f"**Last updated:** {TODAY}  ",
        f"**Scope:** All-India cold-pressed / wood-pressed groundnut oil sellers  ",
        f"**Hyderabad subset:** Tagged Yes in HYD column  ",
        f"",
        f"---",
        f"",
        f"## Evidence rules",
        f"",
        f"- Every row has a source URL and retrieval date",
        f"- Price per litre is always a **Calculation** — original pack + price retained",
        f"- Do not treat a listing, review count, or marketing claim as proof of cold pressing, sales, or current activity",
        f"- If a field is unknown, it shows `—`",
        f"",
        f"---",
        f"",
        f"## Price per litre formula",
        f"",
        f"```",
        f"Price per litre (₹) = Listed price (₹) ÷ Pack size in litres",
        f"Example: ₹480 for 500ml = ₹480 ÷ 0.5 = ₹960/L",
        f"```",
        f"",
        f"---",
        f"",
        f"## Seller data ({len(valid)} products with prices found)",
        f"",
        f"| # | Seller | Type | Product | Pack (ml) | Price (₹) | ₹/L | Process Claim | Variety | Packaging | Rating | Reviews | Channel | HYD | Source | Retrieved | Confidence |",
        f"|---|--------|------|---------|-----------|-----------|-----|---------------|---------|-----------|--------|---------|---------|-----|--------|-----------|------------|",
    ]

    for i, r in enumerate(valid, 1):
        lines.append(
            f"| {i} | {r['seller_name']} | {r['seller_type']} | {r['product_name'][:50]} | "
            f"{r['pack_size_ml']} | {r['listed_price_inr']} | {r['price_per_litre_inr']} | "
            f"{r['process_claim']} | {r['variety_claim']} | {r['packaging_type']} | "
            f"{r['rating']} | {r['review_count']} | {r['channels']} | {r['is_hyderabad']} | "
            f"[link]({r['source_url']}) | {r['retrieved_date']} | {r['confidence']} |"
        )

    lines += [
        f"",
        f"---",
        f"",
        f"## Pages that could not be scraped ({len(errors)} sources)",
        f"",
        f"| Seller | Reason |",
        f"|--------|--------|",
    ]
    for r in errors:
        lines.append(f"| {r['seller_name']} | {r['limitations']} |")

    lines += [
        f"",
        f"---",
        f"",
        f"## Summary (auto-calculated from scraped data)",
        f"",
    ]

    prices = [float(r["price_per_litre_inr"]) for r in valid if r["price_per_litre_inr"] != "—"]
    if prices:
        lines.append(f"- **Price range per litre:** ₹{min(prices):.0f} – ₹{max(prices):.0f}  ")
        lines.append(f"- **Median price per litre:** ₹{sorted(prices)[len(prices)//2]:.0f}  ")
    else:
        lines.append(f"- Price data insufficient for summary  ")

    process_counts: dict[str, int] = {}
    for r in valid:
        for p in r["process_claim"].split(";"):
            p = p.strip()
            if p and p != "—":
                process_counts[p] = process_counts.get(p, 0) + 1
    if process_counts:
        top = sorted(process_counts.items(), key=lambda x: -x[1])
        lines.append(f"- **Process claims found:** {', '.join(f'{k} ({v})' for k,v in top)}  ")

    lines += [
        f"",
        f"---",
        f"",
        f"*Generated by scraper.py — re-run to refresh data.*",
    ]

    return "\n".join(lines)

# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    print(f"2B Research Scraper — {TODAY}")
    print(f"Targets: {len(TARGETS)} sources\n")

    all_rows: list[dict] = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=HEADLESS)

        for seller_name, seller_type, url, strategy, is_hyd in TARGETS:
            print(f"  Scraping: {seller_name} ... ", end="", flush=True)
            # Fresh page per target — prevents cascade navigation errors
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
                locale="en-IN",
            )
            page = await context.new_page()
            try:
                if strategy == "amazon":
                    rows = await scrape_amazon(page, url)
                else:
                    rows = await scrape_generic(page, url, seller_name, seller_type, is_hyd)
                all_rows.extend(rows)
                found = sum(1 for r in rows if r["listed_price_inr"] != "—")
                print(f"{found} products found")
            except Exception as e:
                print(f"ERROR — {e}")
                all_rows.append(_error_row(seller_name, seller_type, url, is_hyd, str(e)[:200]))
            finally:
                await context.close()

        await browser.close()

    # Write CSV
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"\nCSV saved: {CSV_OUT}")

    # Write Markdown
    md_content = rows_to_markdown(all_rows)
    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Markdown saved: {MD_OUT}")

    # Summary
    valid = [r for r in all_rows if r["listed_price_inr"] != "—"]
    print(f"\nTotal products with prices: {len(valid)}")
    print(f"Total sources attempted: {len(TARGETS)}")

if __name__ == "__main__":
    asyncio.run(main())
