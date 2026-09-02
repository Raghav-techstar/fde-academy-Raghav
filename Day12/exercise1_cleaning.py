import pandas as pd


# ============================================================
# EXERCISE 1 - PYTHON CLEANING & DATA QUALITY
# ============================================================

# ------------------------------------------------------------
# Load raw CSV
# ------------------------------------------------------------

df = pd.read_csv("raw_shipments.csv")


# ------------------------------------------------------------
# TASK 1 - PROFILE THE RAW FILE
# ------------------------------------------------------------

print("=" * 60)
print("RAW DATA PROFILE")
print("=" * 60)

print("\nShape:")
print(df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nNull Counts:")
print(df.isnull().sum())

print("\nStatus Values:")
print(df["status"].value_counts(dropna=False))

print("\nDuplicate Shipment IDs:")
print(df["shipment_id"].duplicated().sum())

print("\nRaw Ship Date Range:")
print(df["shipped_date"].min())
print(df["shipped_date"].max())


# ------------------------------------------------------------
# TASK 2 - CLEANING RULES
# ------------------------------------------------------------

cleaning_log = []


# Standardise status
before_status = df["status"].copy()

df["status"] = (
    df["status"]
    .astype("string")
    .str.strip()
    .str.lower()
)

status_map = {
    # No inconsistent variants were found in the raw data.
}

df["status"] = df["status"].replace(status_map)

changed_status = (before_status != df["status"]).sum()

cleaning_log.append(
    f"Standardised status formatting for {changed_status} rows"
)


# ------------------------------------------------------------
# Parse dates
# ------------------------------------------------------------

df["shipped_date"] = pd.to_datetime(
    df["shipped_date"],
    errors="coerce"
)

df["delivered_date"] = pd.to_datetime(
    df["delivered_date"],
    errors="coerce"
)


# Count invalid shipped dates
invalid_ship_dates = df["shipped_date"].isna().sum()

print("\nInvalid shipped dates:")
print(invalid_ship_dates)


# ------------------------------------------------------------
# Drop rows with missing shipment_id or invalid shipped_date
# ------------------------------------------------------------

before = len(df)

df = df.dropna(
    subset=["shipment_id", "shipped_date"]
)

dropped = before - len(df)

cleaning_log.append(
    f"Dropped {dropped} rows: missing shipment_id or unparseable shipped_date"
)


# ------------------------------------------------------------
# Remove duplicate shipment IDs
# ------------------------------------------------------------

before = len(df)

df = df.drop_duplicates(
    subset=["shipment_id"],
    keep="first"
)

dropped = before - len(df)

cleaning_log.append(
    f"Dropped {dropped} duplicate shipment_id rows"
)


# ------------------------------------------------------------
# Flag high-cost outliers
# Do NOT delete them
# ------------------------------------------------------------

cost_threshold = df["cost_usd"].quantile(0.99)

df["cost_flag"] = (
    df["cost_usd"] > cost_threshold
)

cleaning_log.append(
    f"Flagged {df['cost_flag'].sum()} high-cost shipments above the 99th percentile"
)


# ------------------------------------------------------------
# TASK 3 - AUTOMATED DATA QUALITY REPORT
# ------------------------------------------------------------

def data_quality_report(df):

    report = {}

    report["row_count"] = len(df)

    # Null rate for every column
    report["null_rates"] = (
        df.isnull()
        .mean()
        .round(4)
        .to_dict()
    )

    # Duplicate shipment IDs
    report["duplicate_keys"] = (
        df["shipment_id"]
        .duplicated()
        .sum()
    )

    # Negative costs
    report["negative_costs"] = (
        df["cost_usd"] < 0
    ).sum()

    # Maximum null rate
    max_null_rate = max(
        report["null_rates"].values()
    )

    # PASS condition from exercise
    report["PASS"] = (
        report["duplicate_keys"] == 0
        and report["negative_costs"] == 0
        and max_null_rate < 0.05
    )

    return report


# ------------------------------------------------------------
# Print cleaning log
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("CLEANING LOG")
print("=" * 60)

for item in cleaning_log:
    print("-", item)


# ------------------------------------------------------------
# Run DQ report
# ------------------------------------------------------------

report = data_quality_report(df)

print("\n" + "=" * 60)
print("DATA QUALITY REPORT")
print("=" * 60)

print(report)


# ------------------------------------------------------------
# Final cleaned data information
# ------------------------------------------------------------

print("\nFinal Shape:")
print(df.shape)

print("\nFinal Data Types:")
print(df.dtypes)

print("\nFinal Status Values:")
print(df["status"].value_counts())

print("\nFinal Ship Date Range:")
print(df["shipped_date"].min())
print(df["shipped_date"].max())


# ------------------------------------------------------------
# Save cleaned data
# This becomes Exercise 2 input
# ------------------------------------------------------------

df.to_csv(
    "shipments_clean.csv",
    index=False
)

print("\nCleaned data saved as:")
print("shipments_clean.csv")