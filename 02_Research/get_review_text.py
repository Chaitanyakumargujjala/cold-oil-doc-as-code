"""
Fetch Amazon review text by scrolling the customer reviews page.
"""
import asyncio
from datetime import date
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup

TODAY = date.today().isoformat()
OUT = "D:/Cold-Pressed Oil Business/02_Research/review_text.txt"

# ASIN -> seller name
TARGETS = [
    ("B0DVLYNKPQ", "Saffola Cold Pressed Groundnut Oil 1L"),
    ("B00M71172A",  "Pure & Sure Organic Cold Pressed Groundnut Oil 1L"),
    ("B0F4DXDXPR",  "Gem's Gold Cold Pressed Groundnut Oil 1L"),
    ("B0CHY85V8W",  "Anveshan Wood Cold Pressed Groundnut Oil 5L"),
]

async def fetch_reviews(page, asin, name):
    url = f"https://www.amazon.in/product-reviews/{asin}/?sortBy=recent&pageNumber=1"
    lines = [f"\n{'='*60}", f"Product: {name}", f"ASIN: {asin}", f"Retrieved: {TODAY}", ""]
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=25000)
        await page.wait_for_timeout(4000)
        # Scroll to load lazy content
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(2000)

        html = await page.content()
        soup = BeautifulSoup(html, "lxml")

        reviews = soup.select("[data-hook='review']")
        if not reviews:
            lines.append("No reviews found — page may have CAPTCHA or bot block")
            # Save raw snippet for debug
            lines.append(f"Page snippet: {soup.get_text()[:500]}")
            return "\n".join(lines)

        lines.append(f"{len(reviews)} reviews found\n")
        for r in reviews[:10]:
            stars = r.select_one("[data-hook='review-star-rating'] .a-icon-alt")
            title = r.select_one("[data-hook='review-title']")
            body  = r.select_one("[data-hook='review-body']")
            date_el = r.select_one("[data-hook='review-date']")

            s = stars.get_text(strip=True) if stars else "—"
            t = title.get_text(strip=True) if title else "—"
            b = body.get_text(strip=True)[:400] if body else "—"
            d = date_el.get_text(strip=True) if date_el else "—"

            lines.append(f"  [{s}] {t} ({d})")
            lines.append(f"  {b}")
            lines.append("")

    except PlaywrightTimeout:
        lines.append("ERROR: Timeout")
    except Exception as e:
        lines.append(f"ERROR: {e}")

    return "\n".join(lines)


async def main():
    output = [f"2B — Amazon Review Text", f"Date: {TODAY}", ""]

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        for asin, name in TARGETS:
            print(f"  Fetching: {name[:50]}...", end=" ", flush=True)
            ctx = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale="en-IN",
                viewport={"width": 1280, "height": 900},
            )
            pg = await ctx.new_page()
            result = await fetch_reviews(pg, asin, name)
            output.append(result)
            await ctx.close()
            print("done")
        await browser.close()

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print(f"\nSaved: {OUT}")

if __name__ == "__main__":
    asyncio.run(main())
