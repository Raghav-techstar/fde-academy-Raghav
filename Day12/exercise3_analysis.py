# ============================================================================
# Day 12 — Exercise 3: KPI Report & Schema Documentation
# Assumes: Exercise 1 (cleaning) and Exercise 2 (Postgres load + SQL
# transform into shipment_kpi_monthly) are already complete.
# ============================================================================

# %% Setup
import json
import os
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Reuse the same connection from Exercise 2
# NOTE: the password contains '@', which is a reserved character in a
# connection URL -- it must be percent-encoded (@ -> %40) or SQLAlchemy
# will misparse the URL (it'll think the host starts at the '@').
engine = create_engine('postgresql://fde_user:Sep%402026@localhost:5432/fde_academy')


# ============================================================================
# TASK 1: On-Time Rate Trend Chart
# ============================================================================

# %% Query the KPI table back into Python
kpi = pd.read_sql('SELECT * FROM shipment_kpi_monthly', engine)
kpi['ship_month'] = pd.to_datetime(kpi['ship_month'])

# %% Line chart: one line per carrier, sorted by month
fig, ax = plt.subplots(figsize=(9, 4))

for carrier, grp in kpi.groupby('carrier'):
    grp = grp.sort_values('ship_month')
    ax.plot(grp['ship_month'], grp['on_time_rate'], marker='o', label=carrier)

ax.set_title('On-Time Delivery Rate by Carrier')
ax.set_ylabel('On-Time Rate')
ax.set_xlabel('Month')
ax.legend()
plt.tight_layout()
plt.savefig('on_time_rate_by_carrier.png', dpi=150)
plt.close(fig)
print("Saved on_time_rate_by_carrier.png")


# ============================================================================
# TASK 2: Client-Facing KPI Summary (auto-generated from real numbers)
# ============================================================================

# %% Aggregate across the full period, weighted by shipment volume
carrier_summary = (
    kpi.groupby('carrier')
    .apply(lambda g: pd.Series({
        'total_shipments': g['shipment_count'].sum(),
        # volume-weighted on-time rate, not a naive average-of-averages
        'weighted_on_time_rate': (g['on_time_rate'] * g['shipment_count']).sum() / g['shipment_count'].sum(),
        'weighted_avg_freight_cost': (g['avg_freight_cost'] * g['shipment_count']).sum() / g['shipment_count'].sum(),
        'total_high_cost_shipments': g['high_cost_shipments'].sum(),
    }))
    .reset_index()
)

best_carrier = carrier_summary.loc[carrier_summary['weighted_on_time_rate'].idxmax()]
worst_carrier = carrier_summary.loc[carrier_summary['weighted_on_time_rate'].idxmin()]
most_expensive = carrier_summary.loc[carrier_summary['weighted_avg_freight_cost'].idxmax()]

# %% Cost trend: first vs last month in the dataset, overall
monthly_overall = (
    kpi.groupby('ship_month')
    .apply(lambda g: (g['avg_freight_cost'] * g['shipment_count']).sum() / g['shipment_count'].sum())
    .sort_index()
)
first_month, last_month = monthly_overall.index.min(), monthly_overall.index.max()
cost_start, cost_end = monthly_overall.iloc[0], monthly_overall.iloc[-1]
cost_pct_change = (cost_end - cost_start) / cost_start * 100 if cost_start else 0
cost_direction = 'rising' if cost_pct_change > 2 else ('falling' if cost_pct_change < -2 else 'roughly flat')

# %% Pull the Exercise 1 cleaning log if it was persisted; otherwise warn
cleaning_log_path = 'cleaning_log.json'
if os.path.exists(cleaning_log_path):
    with open(cleaning_log_path) as f:
        cleaning_log = json.load(f)
else:
    cleaning_log = None
    print("WARNING: cleaning_log.json not found — Data Quality Caveat below "
          "will use a placeholder. Persist cleaning_log from Exercise 1 to "
          "fix this (see the snippet in the intro).")

dq_caveat_text = (
    "\n".join(f"  - {line}" for line in cleaning_log)
    if cleaning_log else
    "  - [cleaning_log.json not found — re-run Exercise 1 with the log "
    "persisted, then re-run this script to populate real drop counts here]"
)

# %% Compose the summary — plain business language, real numbers, no code/SQL
kpi_summary = f"""\
KPI SUMMARY -- Shipment Performance
Prepared for: Client Operations Director
Generated: {datetime.now():%Y-%m-%d}

1. On-Time Delivery:
   {best_carrier['carrier']} is our strongest performer at
   {best_carrier['weighted_on_time_rate']*100:.1f}% on-time delivery across
   {int(best_carrier['total_shipments'])} shipments. {worst_carrier['carrier']}
   trails at {worst_carrier['weighted_on_time_rate']*100:.1f}%, a gap of
   {(best_carrier['weighted_on_time_rate'] - worst_carrier['weighted_on_time_rate'])*100:.1f}
   percentage points -- worth a direct conversation with {worst_carrier['carrier']}
   about root cause before we scale volume with them further.

2. Freight Cost:
   Average freight cost is {cost_direction} across the period, moving from
   ${cost_start:,.2f} in {first_month:%B %Y} to ${cost_end:,.2f} in
   {last_month:%B %Y} ({cost_pct_change:+.1f}%). {most_expensive['carrier']} runs
   the highest average cost per shipment at ${most_expensive['weighted_avg_freight_cost']:,.2f},
   with {int(most_expensive['total_high_cost_shipments'])} shipments flagged as
   statistical cost outliers (above the 99th percentile) for follow-up.

3. Data Quality Caveat:
   Before analysis, the raw weekly export required cleaning. Rows were
   dropped or fixed for the following reasons:
{dq_caveat_text}
   These figures reflect the data AFTER cleaning. If the drop rate above
   exceeds roughly 10% of the original file, treat these KPIs as directional
   rather than final, and flag the drop rate itself to the client as a
   source-data quality issue worth fixing at the TMS level, not just a
   pipeline concern.
"""

print(kpi_summary)
with open('kpi_summary.md', 'w') as f:
    f.write(kpi_summary)
print("Saved kpi_summary.md")


# ============================================================================
# TASK 3: Schema & Lineage Document
# ============================================================================

# %% Pull actual row counts to ground the lineage doc in real numbers
with engine.connect() as conn:
    clean_row_count = pd.read_sql('SELECT COUNT(*) AS n FROM shipments_clean', conn)['n'][0]
    kpi_row_count = pd.read_sql('SELECT COUNT(*) AS n FROM shipment_kpi_monthly', conn)['n'][0]

schema_lineage_doc = f"""\
DATASET: shipment_kpi_monthly
SOURCE: raw_shipments.csv
GENERATED: {datetime.now():%Y-%m-%d}

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
  -> shipments_clean (PostgreSQL table, {clean_row_count} rows)
       Loaded via df.to_sql('shipments_clean', engine, if_exists='replace',
       index=False).
  -> SQL aggregation:
       GROUP BY carrier, DATE_TRUNC('month', ship_date). Computes
       shipment_count, avg_freight_cost, on_time_rate (share of rows where
       status = 'delivered'), and high_cost_shipments (COUNT(*) FILTER
       WHERE cost_flag).
  -> shipment_kpi_monthly (PostgreSQL table, {kpi_row_count} rows)

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
{dq_caveat_text}
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
"""

print(schema_lineage_doc)
with open('schema_lineage.md', 'w') as f:
    f.write(schema_lineage_doc)
print("Saved schema_lineage.md")
