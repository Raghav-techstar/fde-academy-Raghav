import pandas as pd
from pathlib import Path

# TASK 2A
def load_shipments(file_path: str) -> pd.DataFrame:
    if not Path(file_path).exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    df = pd.read_csv(file_path, skipinitialspace=True)

    df = df.dropna(how='all')
    df = df.reset_index(drop=True)
    return df

# TASK 2B
VALID_STATUSES = {"in_transit", "delivered", "pending", "exception"}
VALID_CARRIERS = {"DHL", "FEDEX", "BLUEDART"}

def normalise_row(row: pd.Series) -> pd.Series:
    """
    Normalise string fields in a single row:
    - shipment_id: strip whitespace
    - carrier: strip, convert to UPPER
    - status: strip, convert to lower
    - origin: strip, convert to Title Case
    - destination: strip, convert to Title Case
    - delay_days: coerce to int; set to None if not numeric
    - cost_usd: coerce to float; set to None if not numeric

    Returns the modified row (pd.Series).
    """

    # shipment_id
    row["shipment_id"] = (
        str(row["shipment_id"]).strip()
        if pd.notna(row["shipment_id"])
        else None
    )

    # carrier
    row["carrier"] = (
        str(row["carrier"]).strip().upper()
        if pd.notna(row["carrier"])
        else None
    )

    # status
    row["status"] = (
        str(row["status"]).strip().lower()
        if pd.notna(row["status"])
        else None
    )

    # origin
    row["origin"] = (
        str(row["origin"]).strip().title()
        if pd.notna(row["origin"])
        else None
    )

    # destination
    row["destination"] = (
        str(row["destination"]).strip().title()
        if pd.notna(row["destination"])
        else None
    )

    # delay_days
    delay = pd.to_numeric(row["delay_days"], errors="coerce")
    row["delay_days"] = int(delay) if pd.notna(delay) else None

    # cost_usd
    cost = pd.to_numeric(row["cost_usd"], errors="coerce")
    row["cost_usd"] = float(cost) if pd.notna(cost) else None

    return row

 # TASK 2C
def validate_row(row: pd.Series) -> list[str]:
    errors = []

    if pd.isna(row["shipment_id"]) or str(row["shipment_id"]).strip() == "":
        errors.append ("Missing shipment_id")

    if row["carrier"] not in VALID_CARRIERS:
        errors.append ("Invalid carrier")

    if row["status"] not in VALID_STATUSES:
        errors.append ("Invalid status")

    if row["delay_days"] is None or pd.isna(row["delay_days"]):
        errors.append("Invalid delay_days")
    elif row["delay_days"] < 0:
        errors.append("Negative delay_days")

    if row["cost_usd"] is None or pd.isna(row["cost_usd"]):
        errors.append("Invalid cost_usd")
    elif row["cost_usd"] <=0:
        errors.append("Invalid cost_usd")

    return errors


# TASK 3
def clean_shipments(
    input_path: str,
    clean_output_path: str,
    rejected_output_path: str,
) -> dict:
    """
    Run the complete shipment cleaning pipeline.

    Returns:
        Dictionary containing summary statistics.
    """

    # Load the raw CSV
    df = load_shipments(input_path)

    df = df.apply(normalise_row, axis=1)

    clean_rows = []
    rejected_rows = []

    rejection_reasons = set()

    # Validate every row
    for _, row in df.iterrows():
        row = row.copy()

        errors = validate_row(row)

        if not errors:
            clean_rows.append(row)
        else:
            row["rejection_reasons"] = ", ".join(errors)
            rejected_rows.append(row)
            rejection_reasons.update(errors)

    # Convert lists into DataFrames
    clean_df = pd.DataFrame(clean_rows)
    rejected_df = pd.DataFrame(rejected_rows)

    # Save CSV files
    clean_df.to_csv(clean_output_path, index=False)
    rejected_df.to_csv(rejected_output_path, index=False)

    # Calculate statistics
    total_input = len(df)
    clean_count = len(clean_df)
    rejected_count = len(rejected_df)

    rejection_rate_pct = round(
        (rejected_count / total_input) * 100, 1
    ) if total_input else 0.0

    summary = {
        "total_input": total_input,
        "clean_count": clean_count,
        "rejected_count": rejected_count,
        "rejection_rate_pct": rejection_rate_pct,
        "rejection_reasons": sorted(list(rejection_reasons)),
    }

    return summary

if __name__ == "__main__":

    summary = clean_shipments(
        input_path="shipments_raw.csv",
        clean_output_path="shipments_clean.csv",
        rejected_output_path="shipments_rejected.csv",
    )

    print("\n=== Data Quality Report ===")

    for key, value in summary.items():
        print(f"{key:<25} {value}")
