import csv
import sys

out = open('D:/Cold-Pressed Oil Business/02_Research/results_summary.txt', 'w', encoding='utf-8')

def p(s=''):
    out.write(s + '\n')

with open('D:/Cold-Pressed Oil Business/02_Research/scraped_data.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

DASH = "\u2014"
valid = [r for r in rows if r['listed_price_inr'] not in ('', DASH, '--')]
errors = [r for r in rows if r['listed_price_inr'] in ('', DASH, '--')]

p(f"Total rows: {len(rows)}")
p(f"Products with prices: {len(valid)}")
p(f"Inaccessible/no data: {len(errors)}")
p()

p("=== PRODUCTS WITH PRICES ===")
for r in valid:
    p(f"  Seller: {r['seller_name']}")
    p(f"  Product: {r['product_name']}")
    p(f"  Pack: {r['pack_size_ml']}ml | Price: Rs{r['listed_price_inr']} | Per litre: Rs{r['price_per_litre_inr']}")
    p(f"  Process: {r['process_claim']} | Packaging: {r['packaging_type']}")
    p(f"  Rating: {r['rating']} | Reviews: {r['review_count']}")
    p(f"  Source: {r['source_url']}")
    p(f"  Confidence: {r['confidence']}")
    p()

p("=== INACCESSIBLE SOURCES ===")
for r in errors:
    p(f"  {r['seller_name']} | {r['limitations']}")

out.close()
print("Written to results_summary.txt")
