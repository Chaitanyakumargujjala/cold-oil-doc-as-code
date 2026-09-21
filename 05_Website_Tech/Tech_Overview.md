# 2B — Website Tech Overview

**Last updated:** 2026-09-20  
**Status:** Direction confirmed — implementation not started

---

## Tech stack

| Layer | Decision | Status |
|-------|----------|--------|
| Frontend | React + TypeScript | Confirmed |
| Design approach | Mobile-first | Confirmed |
| Checkout | Guest only — no login | Confirmed |
| Payment | Online + COD | Confirmed |
| Notifications | Email-first | Confirmed |
| Hosting | AWS Amplify | Under evaluation |
| Delivery integration | Shiprocket or similar | Under evaluation |
| Payment provider | Razorpay / Cashfree / PayU — TBD | Open decision T1 |
| Domain | TBD | Open decision T4 |

---

## Existing assets

| Asset | Location | Notes |
|-------|----------|-------|
| React source | `cold-oil-react-assets` GitHub repo | Exists — not yet reviewed |
| Sample batch page | `GN-2026-0042` | Built for testing QR concept |
| Previous hosted URL | `traceable-oils-hyderabad.cgujjala.chatgpt.site` | Temporary — not production |

---

## QR traceability design

- One QR code per production batch
- QR encodes a short permanent identifier only (e.g. `2b.in/b/GN-2026-0042`)
- Identifier never reused
- QR points to a 2B-controlled URL — not a third-party hosting URL
- Customer-facing batch page shows: variety, origin, press date, press method, lab results (if available)
- QR goes on the bottle label — must be decided before labels are printed

---

## V1 website — page structure

```
Home / Product page
  └── Add to cart
      └── Cart
          └── Checkout (guest — name, address, phone, email)
              └── Payment (online or COD)
                  └── Order confirmation (email sent)
                      └── [Admin: order management]
```

---

## Implementation priority

Website work starts **after**:
1. Competitor research complete
2. Selling price decided
3. Packaging spec confirmed
4. At least one supply source identified

Do not build before the above are done — the product page copy and pricing depend on research outputs.
