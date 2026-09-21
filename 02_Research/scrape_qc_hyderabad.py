"""
2B — Quick-commerce + Hyderabad scraper
Targets: BigBasket, Blinkit, Zepto, Swiggy Instamart, Hyderabad brand sites
Output: qc_hyderabad_data.txt
"""
import asyncio
import re
from datetime import date
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup

TODAY = date.today().isoformat()
OUT = "D:/Cold-Pressed Oil Business/02_Research/qc_hyderabad_data.txt"

TARGETS = [
    # Quick-commerce
    ("BigBasket",        "https://www.bigbasket.com/ps/?q=cold+pressed+groundnut+oil&nc=as"),
    ("Blinkit",          "https://blinkit.com/s/?q=cold%20pressed%20groundnut%20oil"),
    ("Zepto",            "https://www.zeptonow.com/search?query=cold+pressed+groundnut+oil"),
    ("Swiggy Instamart", "https://www.swiggy.com/instamart/search?query=cold+pressed+groundnut+oil"),
    # Hyderabad-specific brands
    ("Sneha Ganuga Oils","https://www.snehaganugafoods.com"),
    ("Siri Organics HYD","https://www.siriorganics.in"),
    ("Praakritik HYD",   "https://www.praakritik.com/collections/all"),
    # Amazon Hyderabad-specific search
    ("Amazon - ganuga",  "https://www.amazon.in/s?k=ganuga+groundnut+oil+hyderabad"),
    ("Amazon - chekku HYD", "https://www.amazon.in/s?k=chekku+groundnut+oil+hyderabad"),
]

PROCESS_TERMS = ["cold-pressed","cold pressed","wood pressed","wood-pressed",
                 "kachi ghani","chekku","ganuga","wooden ghani","expeller"]

def detect_process(text):
    text_lower = text.lower()
    found = [t for t in PROCESS_TERMS if t in text_lower]
    return "; ".join(found) if found else "—"

def extract_price(text):
    text = text.replace(",","")
    m = re.search(r"[₹\u20b9Rs\.]*\s*(\d+(?:\.\d+)?)", text)
    return float(m.group(1)) if m else None

def extract_pack_ml(text):
    text = text.lower()
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:litre|ltr|liter|l)\b", text)
    if m: return int(float(m.group(1)) * 1000)
    m = re.search(r"(\d+)\s*(?:ml|millilitre)", text)
    if m: return int(m.group(1))
    m = re.search(r"\b(250|500|750|1000|1500|2000|3000|5000)\b", text)
    if m: return int(m.group(1))
    return None

async def scrape_page(page, name, url):
    lines = [f"\n{'='*60}", f"SOURCE: {name}", f"URL: {url}", f"Date: {TODAY}", ""]
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=25000)
        await page.wait_for_timeout(4000)
        # Scroll to trigger lazy loading
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        await page.wait_for_timeout(2000)
        html = await page.content()
        soup = BeautifulSoup(html, "lxml")
        full_text = soup.get_text(" ", strip=True)

        # Check if page loaded properly
        if len(full_text) < 200:
            lines.append("Page too short — likely blocked or empty")
            lines.append(f"Snippet: {full_text[:300]}")
            return "\n".join(lines)

        # Look for groundnut/peanut mentions with prices nearby
        lines.append("--- GROUNDNUT PRODUCT MENTIONS ---")
        chunks = re.findall(r'.{0,100}(?:groundnut|peanut|moongphali|pallilu).{0,100}',
                           full_text, re.I)
        if chunks:
            for c in chunks[:10]:
                lines.append(f"  {c.strip()}")
        else:
            lines.append("  No groundnut mentions found")

        lines.append("")
        lines.append("--- PRICE MENTIONS ---")
        price_chunks = re.findall(r'.{0,50}(?:₹|Rs\.?)\s*\d[\d,]+.{0,50}', full_text)
        if price_chunks:
            for c in price_chunks[:10]:
                lines.append(f"  {c.strip()}")
        else:
            lines.append("  No price mentions found")

        lines.append("")
        lines.append("--- PROCESS CLAIM MENTIONS ---")
        process_found = detect_process(full_text)
        lines.append(f"  {process_found}")

        # Try to find structured product cards
        lines.append("")
        lines.append("--- PRODUCT CARDS (if found) ---")
        cards = soup.select(
            ".product-card, .product-item, [class*='product'], "
            "[class*='item-card'], [class*='ProductCard'], "
            "[data-testid*='product'], .plp-product, .shelf-item"
        )
        gn_cards = [c for c in cards if
                    any(w in c.get_text().lower()
                        for w in ["groundnut","peanut","moongphali"])]
        if gn_cards:
            for card in gn_cards[:8]:
                card_text = card.get_text(" ", strip=True)
                price_m = re.search(r'[₹\u20b9]\s*(\d[\d,]+)', card_text)
                price = price_m.group(0) if price_m else "—"
                lines.append(f"  [{price}] {card_text[:120]}")
        else:
            lines.append("  No structured product cards found")

    except PlaywrightTimeout:
        lines.append("ERROR: Page timed out")
    except Exception as e:
        lines.append(f"ERROR: {e}")

    return "\n".join(lines)


async def main():
    output = [f"2B — Quick-Commerce + Hyderabad Research", f"Date: {TODAY}", ""]

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)

        for name, url in TARGETS:
            print(f"  Scraping: {name}...", end=" ", flush=True)
            ctx = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/120.0.0.0 Safari/537.36",
                locale="en-IN",
                viewport={"width": 1280, "height": 900},
                geolocation={"latitude": 17.3850, "longitude": 78.4867},  # Hyderabad
                permissions=["geolocation"],
            )
            pg = await ctx.new_page()
            result = await scrape_page(pg, name, url)
            output.append(result)
            await ctx.close()
            print("done")

        await browser.close()

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print(f"\nSaved: {OUT}")

if __name__ == "__main__":
    asyncio.run(main())
