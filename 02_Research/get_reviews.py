"""
2B — Amazon Review Scraper + Brand Gap Fill
Fetches reviews from top Amazon sellers and remaining brand pages.
Output: review_data.txt
"""

import asyncio
import re
from datetime import date
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

TODAY = date.today().isoformat()
OUT = "D:/Cold-Pressed Oil Business/02_Research/review_data.txt"

REVIEW_TARGETS = [
    ("Saffola",     "https://www.amazon.in/dp/B0DVLYNKPQ"),
    ("Pure & Sure", "https://www.amazon.in/dp/B00M71172A"),
    ("Gem's Gold",  "https://www.amazon.in/dp/B0F4DXDXPR"),
    ("Anveshan 5L", "https://www.amazon.in/dp/B0CHY85V8W"),
]

BRAND_GAPS = [
    ("Praakritik",  "https://www.praakritik.com/collections/all"),
    ("Nutriorg",    "https://www.nutriorg.com/collections/all"),
    ("Gramiyum",    "https://gramiyum.com/product-category/oils/groundnut-oil/"),
    ("Jivika",      "https://www.jivikaorganics.com/product/cold-pressed-groundnut-oil/"),
]

async def get_amazon_reviews(page, seller, url):
    lines = [f"\n{'='*60}", f"SELLER: {seller}", f"URL: {url}", f"Retrieved: {TODAY}", ""]
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=25000)
        await page.wait_for_timeout(3000)

        # Try to accept cookies / dismiss popups
        try:
            await page.click("input[id='sp-cc-accept']", timeout=3000)
        except:
            pass

        html = await page.content()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "lxml")

        # Product title
        title = soup.select_one("#productTitle")
        if title:
            lines.append(f"Product: {title.get_text(strip=True)[:100]}")

        # Price
        price = soup.select_one(".a-price .a-offscreen, #priceblock_ourprice, .a-price-whole")
        if price:
            lines.append(f"Price: {price.get_text(strip=True)}")

        # Rating summary
        rating = soup.select_one("[data-hook='rating-out-of-text'], #acrPopover")
        if rating:
            lines.append(f"Rating: {rating.get_text(strip=True)}")

        review_count = soup.select_one("[data-hook='total-review-count'], #acrCustomerReviewText")
        if review_count:
            lines.append(f"Reviews: {review_count.get_text(strip=True)}")

        lines.append("")

        # Reviews
        reviews = soup.select("[data-hook='review'], .review")
        if not reviews:
            lines.append("No reviews parsed — page may require JS or login")
        else:
            lines.append(f"--- TOP REVIEWS ({len(reviews)} found) ---")
            for r in reviews[:8]:
                rating_el = r.select_one("[data-hook='review-star-rating'] .a-icon-alt, .review-rating .a-icon-alt")
                body_el = r.select_one("[data-hook='review-body'] span, .review-text")
                title_el = r.select_one("[data-hook='review-title'] span:not(.a-icon-alt)")

                r_rating = rating_el.get_text(strip=True) if rating_el else "—"
                r_title = title_el.get_text(strip=True) if title_el else "—"
                r_body = body_el.get_text(strip=True)[:300] if body_el else "—"

                lines.append(f"  [{r_rating}] {r_title}")
                lines.append(f"  {r_body}")
                lines.append("")

    except PlaywrightTimeout:
        lines.append("ERROR: Page timed out")
    except Exception as e:
        lines.append(f"ERROR: {e}")

    return "\n".join(lines)


async def get_brand_page(page, seller, url):
    lines = [f"\n{'='*60}", f"SELLER: {seller}", f"URL: {url}", f"Retrieved: {TODAY}", ""]
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(2000)
        html = await page.content()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "lxml")

        # Find any groundnut product + price
        text = soup.get_text(" ", strip=True)
        # Look for price patterns near "groundnut" or "peanut"
        chunks = re.findall(r'.{0,60}(?:groundnut|peanut).{0,60}', text, re.I)
        price_chunks = re.findall(r'.{0,40}(?:Rs\.?|₹)\s*[\d,]+.{0,40}', text)

        lines.append("GROUNDNUT MENTIONS:")
        for c in chunks[:5]:
            lines.append(f"  {c.strip()}")
        lines.append("")
        lines.append("PRICE MENTIONS:")
        for c in price_chunks[:8]:
            lines.append(f"  {c.strip()}")

    except PlaywrightTimeout:
        lines.append("ERROR: Timeout")
    except Exception as e:
        lines.append(f"ERROR: {e}")

    return "\n".join(lines)


async def main():
    output = [f"2B Research — Reviews & Brand Gap Fill", f"Date: {TODAY}", ""]

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)

        print("Fetching Amazon reviews...")
        for seller, url in REVIEW_TARGETS:
            print(f"  {seller}...", end=" ", flush=True)
            ctx = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale="en-IN", viewport={"width": 1280, "height": 900}
            )
            pg = await ctx.new_page()
            result = await get_amazon_reviews(pg, seller, url)
            output.append(result)
            await ctx.close()
            print("done")

        print("Fetching brand gap pages...")
        for seller, url in BRAND_GAPS:
            print(f"  {seller}...", end=" ", flush=True)
            ctx = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale="en-IN", viewport={"width": 1280, "height": 900}
            )
            pg = await ctx.new_page()
            result = await get_brand_page(pg, seller, url)
            output.append(result)
            await ctx.close()
            print("done")

        await browser.close()

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print(f"\nSaved to {OUT}")

if __name__ == "__main__":
    asyncio.run(main())
