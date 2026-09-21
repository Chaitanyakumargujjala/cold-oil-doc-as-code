# 2B — Market Research Master

**Last updated:** 2026-09-20  
**Purpose:** Research questions, method, and outputs that feed business decisions

---

## Key questions — status after Initial scrape

| # | Question | Feeds into | Status | Finding |
|---|----------|-----------|--------|---------|
| R1 | What is the price range per litre? | Pricing decision | **Done** | ₹287–₹564/L (1L pack). Comparable premium (glass, artisan): ₹349–₹564/L |
| R2 | Who are the major all-India players? | Positioning | **Done** | Anveshan, Saffola, Tata Simply Better, Pure & Sure, Hesthetic, Puvi, Fresh & Crush, Gem's Gold |
| R3 | What process claims are common? | Claims strategy | **Done** | "Cold-pressed" universal; "chekku/kachi ghani/ganuga" common on Amazon; wood-pressed less common |
| R4 | What do customers complain about most? | Product and packaging decisions | **Partial** | Tin leakage (Anveshan), price vs FMCG, purity questions. Full review text blocked by Amazon login |
| R5 | Which pack sizes sell best? | Pack size decision | **Partial** | 1L most common; 5L bulk popular on Amazon; Blinkit shows 1L as dominant quick-commerce size |
| R6 | What packaging formats are common? | Packaging decision | **Done** | Plastic dominant; glass available (Anveshan ₹564, Hesthetic ₹349); steel tin at 5L only |
| R7 | Which variety do competitors use? | Variety decision | **Done** | Nobody names Java/Bold/Tac publicly — this is a gap 2B can own |
| R8 | What delivery fees do competitors charge? | Delivery fee decision | **Partial** | Free above ₹499–₹899 on own websites; Blinkit has no delivery fee (platform handles it) |
| R9 | Which channels do competitors sell on? | Channel strategy | **Done** | All major brands on Amazon + own website; top brands on Blinkit; no purely website-only brand found |
| R10 | What is the Hyderabad-specific picture? | Launch city decision | **Partial** | Blinkit Hyderabad has 10 cold-pressed GN oil products. No local Hyderabad brand found online. Local mills (ganuga/chekku) operate via Instagram/WhatsApp only |

---

## Research outputs

| Output | File | Status |
|--------|------|--------|
| All-India competitor price table | `02_Research/Competitor_Research.md` | **Complete** — 28 products, 15 sellers |
| Blinkit Hyderabad prices | Same file — Quick-commerce section | **Complete** |
| Hyderabad local sellers | Same file — Hyderabad section | **Partial** — no web presence found; Instagram research needed |
| Unit economics model | `04_Financials/Unit_Economics.md` | Not started — waiting on Sneha Ganuga quote |
| Product spec decisions | `03_Product/Groundnut_Oil_v1.md` | Not started — waiting on home test |
| Packaging decision | `03_Product/Groundnut_Oil_v1.md` | Not started — waiting on home test + sample |

---

## Market context — confirmed findings (Initial scrape)

### Pricing
- **Observed evidence:** FMCG cold-pressed floor is ₹287–₹340/L (Dabur, Saffola, Tata)
- **Observed evidence:** Artisan cold-pressed plastic bottle: ₹330–₹425/L
- **Observed evidence:** Artisan cold-pressed glass bottle: ₹349–₹564/L
- **Observed evidence:** Blinkit discounts MRP by 9–42% — customers expect platform discounts
- **Assumption updated:** Market is fragmented — confirmed. No single dominant brand.
- **Assumption updated:** Premium cold-pressed sells at a significant premium to refined — confirmed. Refined groundnut oil is ~₹100–₹150/L; cold-pressed commands 2–4x.

### Competition
- **Observed evidence:** Anveshan is the strongest artisan brand — 1277 reviews, 4.8 stars, lab-tested, Gujarat + Tamil Nadu sourcing, glass + plastic + steel options
- **Observed evidence:** Puvi has 6,100 reviews and 600+ orders/month — highest volume artisan seller found
- **Observed evidence:** Saffola, Tata, Dabur are all in "cold-pressed" segment — large FMCG brands commoditising the claim
- **Observed evidence:** Fresh & Crush (Madurai, since 1954) — sells wood-pressed and steel-pressed, currently sold out, free delivery above ₹899

### What nobody is doing (gap for 2B)
- **Observed evidence:** No competitor names a specific groundnut variety (Java/Bold/Tac) publicly
- **Observed evidence:** No competitor offers QR batch traceability to a customer-facing page
- **Observed evidence:** No competitor is Hyderabad-origin with a direct story to local customers

### Packaging
- **Observed evidence:** Glass bottle commands ₹139/L premium over plastic in same brand (Anveshan)
- **Observed evidence:** Steel tin only seen at 5L+ bulk packs — not at 1L
- **Observed evidence:** Plastic is dominant at all price points

### Quick-commerce
- **Observed evidence:** Cold-pressed groundnut oil available on Blinkit Hyderabad with 8-min delivery
- **Observed evidence:** 10+ products available; Anveshan, Tata, Saffola, Gulab, Organic India all listed
- **Implication:** 2B cannot compete on speed or convenience — must compete on trust, story, and traceability

---

## Groundnut variety notes

| Variety | Also known as | Key characteristic | Status |
|---------|--------------|-------------------|--------|
| Java | — | Smaller kernel, higher oil content | Needs verification from supplier |
| Bold | — | Larger kernel, popular in Gujarat | Needs verification from supplier |
| Tac | — | Terminology unclear — regional/trade term? | **Unknown — verify with Sneha Ganuga before any claim** |

**No competitor names a specific variety. This is a confirmed gap 2B can own.**  
Do not make variety-specific claims until confirmed by supplier documentation.

---

## What remains to be researched

| Topic | Why it matters | How to get it |
|-------|---------------|---------------|
| Hyderabad local mills (Instagram) | Direct local competitors; pricing; customer relationship style | Manual Instagram search: "ganuga oil hyderabad", "chekku oil hyderabad" |
| Full Amazon review text | Customer complaints and praise in detail | Requires Amazon login — manual reading recommended |
| Flipkart prices | May differ from Amazon; different customer segment | Manual check |
| Zepto / Swiggy Instamart | Quick-commerce pricing and availability | Manual check on app |
| Wood Press brand | Reportedly a major player — site unreachable | Try woodpressedoil.com later or check Amazon listing |
| Sneha Ganuga seed prices | Feeds unit economics | Call/WhatsApp directly |
