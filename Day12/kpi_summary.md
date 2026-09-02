KPI SUMMARY -- Shipment Performance
Prepared for: Client Operations Director
Generated: 2026-09-02

1. On-Time Delivery:
   DHL is our strongest performer at
   7.9% on-time delivery across
   37539 shipments. FEDEX
   trails at 7.7%, a gap of
   0.2
   percentage points -- worth a direct conversation with FEDEX
   about root cause before we scale volume with them further.

2. Freight Cost:
   Average freight cost is roughly flat across the period, moving from
   $271.00 in January 2024 to $269.01 in
   June 2024 (-0.7%). DHL runs
   the highest average cost per shipment at $269.71,
   with 396 shipments flagged as
   statistical cost outliers (above the 99th percentile) for follow-up.

3. Data Quality Caveat:
   Before analysis, the raw weekly export required cleaning. Rows were
   dropped or fixed for the following reasons:
  - [cleaning_log.json not found — re-run Exercise 1 with the log persisted, then re-run this script to populate real drop counts here]
   These figures reflect the data AFTER cleaning. If the drop rate above
   exceeds roughly 10% of the original file, treat these KPIs as directional
   rather than final, and flag the drop rate itself to the client as a
   source-data quality issue worth fixing at the TMS level, not just a
   pipeline concern.
