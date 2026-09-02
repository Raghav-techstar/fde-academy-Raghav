DATASET: shipment_kpi_monthly
SOURCE: raw_shipments.csv
GENERATED: 2026-09-02

LINEAGE:
  raw_shipments.csv
  -> Python cleaning (pandas):
       1. Standardise `status`: strip whitespace, lowercase, then map known
          variants (e.g. 'in-transit', 'IN_TRANSIT') to a canonical set
          (e.g. 'in_transit') via an explicit status_map dict.
       2. Parse `ship_date` with pd.to_datetime(errors='coerce'); rows that
          fail to parse become NaT and are dropped in the next step.
       3. Drop rows with a missing shipment_id OR an unparseable ship_date
          (logged count: see cleaning_log below).
       4. Drop duplicate shipment_id rows, keep='first' (logged count: see
          cleaning_log below).
       5. Flag (not drop) freight_cost outliers above the 99th percentile
          into a boolean `cost_flag` column — outliers stay in the dataset
          and stay in every downstream average unless explicitly excluded.
  -> shipments_clean (PostgreSQL table, 100000 rows)
       Loaded via df.to_sql('shipments_clean', engine, if_exists='replace',
       index=False).
  -> SQL aggregation:
       GROUP BY carrier, DATE_TRUNC('month', ship_date). Computes
       shipment_count, avg_freight_cost, on_time_rate (share of rows where
       status = 'delivered'), and high_cost_shipments (COUNT(*) FILTER
       WHERE cost_flag).
  -> shipment_kpi_monthly (PostgreSQL table, 18 rows)

SCHEMA:
  carrier               VARCHAR   Carrier code/name as it appears in the
                                   source TMS export (post status/carrier
                                   normalisation from cleaning step 1).
  ship_month            DATE      First day of the calendar month the
                                   shipment's ship_date falls in
                                   (DATE_TRUNC('month', ship_date)).
  shipment_count         INTEGER   Count of cleaned shipment rows for this
                                   carrier + month.
  avg_freight_cost       NUMERIC   Mean freight_cost across this carrier's
                                   shipments in this month, INCLUDING any
                                   rows flagged by cost_flag (outliers are
                                   flagged, not excluded from this average).
  on_time_rate           FLOAT     Share of this carrier/month's shipments
                                   with status = 'delivered', range 0.0-1.0.
  high_cost_shipments    INTEGER   Count of shipments this carrier/month
                                   with freight_cost above the 99th
                                   percentile of the full cleaned dataset
                                   (not a per-carrier or per-month
                                   percentile — one global threshold).

KNOWN LIMITATIONS:
  - [cleaning_log.json not found — re-run Exercise 1 with the log persisted, then re-run this script to populate real drop counts here]
  - avg_freight_cost includes flagged cost outliers; if the client wants a
    trimmed average excluding those, that's a follow-up transform, not
    something this table currently provides.
  - The status_map built in Exercise 1 only covers variants observed in
    THIS week's file. A future weekly drop could contain an unseen status
    variant that won't get mapped to a canonical value — recommend adding
    a catch-all / unmapped-status alert to the pipeline before this goes
    into production use.
  - high_cost_shipments uses one global 99th-percentile threshold computed
    once at cleaning time; it does not update as new weekly files arrive,
    so its meaning will drift if freight costs trend up or down over time.
