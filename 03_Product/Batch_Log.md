# 2B — Batch Log

**Last updated:** 2026-09-20  
**Purpose:** Record every production batch for traceability and QR linking

---

## Batch format

Batch IDs follow the format: `GN-YYYY-NNNN`  
Example: `GN-2026-0042`  
- `GN` = Groundnut  
- `YYYY` = Year  
- `NNNN` = Sequential batch number, never reused

---

## Batch records

| Batch ID     | Date Pressed | Variety | Supplier / Farm | Press Location | Press Method | Volume (L) | Bottles Filled | Packaging | QR Live?    | Notes                       |
| ------------ | ------------ | ------- | --------------- | -------------- | ------------ | ---------- | -------------- | --------- | ----------- | --------------------------- |
| GN-2026-0042 | —            | —       | —               | —              | —            | —          | —              | —         | Sample only | Sample batch for QR testing |

*No real batches yet. Add a row for every new batch.*

---

## QR batch page fields

When a batch QR goes live, the customer-facing page should show:

- Batch ID
- Groundnut variety
- Farm or supplier name and location (state/district level)
- Date pressed
- Press method (cold-pressed / wood-pressed / etc.)
- Bottled by
- Lab test results (if available)
- Best before date

**Do not publish a QR page without at minimum: batch ID, variety, press date, and press method confirmed by supplier documentation.**
