# TASK 1
"""
AutoFinance Bank — Daily Shipment Operations Report
FDE Academy Day 3 Exercise 3

Usage:
    python day3_ex3_report.py

Outputs:
    - Console: formatted KPI report
    - shipments_summary.csv: per-carrier aggregated KPIs
    - route_report.csv: top routes by volume
"""
import pandas as pd
from pathlib import Path
from datetime import date

INPUT_FILE   = "shipments_clean.csv"
SUMMARY_CSV  = "shipments_summary.csv"
ROUTES_CSV   = "route_report.csv"


# TASK 2A
def compute_carrier_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute per-carrier KPIs from the cleaned shipments DataFrame.

    Returns a DataFrame with columns:
        carrier
        total_shipments
        delivered
        in_transit
        otif_pct
        avg_delay_days
        max_delay_days
        total_revenue
        avg_cost_per_ship
    """

    carrier_summary = []

    # Group data by carrier
    grouped = df.groupby("carrier")

    for carrier, group in grouped:

        total_shipments = len(group)

        delivered = (group["status"] == "delivered").sum()

        in_transit = (group["status"] == "in_transit").sum()

        # On-Time In-Full (Delivered with zero delay)
        on_time = (
            (group["status"] == "delivered")
            & (group["delay_days"] == 0)
        ).sum()

        otif_pct = round((on_time / total_shipments) * 100, 1)

        avg_delay_days = round(group["delay_days"].mean(), 1)

        max_delay_days = int(group["delay_days"].max())

        total_revenue = round(group["cost_usd"].sum(), 2)

        avg_cost_per_ship = round(group["cost_usd"].mean(), 2)

        carrier_summary.append(
            {
                "carrier": carrier,
                "total_shipments": total_shipments,
                "delivered": delivered,
                "in_transit": in_transit,
                "otif_pct": otif_pct,
                "avg_delay_days": avg_delay_days,
                "max_delay_days": max_delay_days,
                "total_revenue": total_revenue,
                "avg_cost_per_ship": avg_cost_per_ship,
            }
        )

    # Convert to DataFrame
    result = pd.DataFrame(carrier_summary)

    # Sort by shipment count (highest first)
    result = result.sort_values(
        by="total_shipments",
        ascending=False
    ).reset_index(drop=True)

    return result


# TASK 2B
def compute_route_report(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Compute a route-level report grouped by (origin, destination).

    Returns a DataFrame with columns:
        route
        shipment_count
        avg_delay_days
        total_revenue
        most_used_carrier

    Returns only the top_n routes by shipment_count.
    """

    route_summary = []

    # Group by origin and destination
    grouped = df.groupby(["origin", "destination"])

    for (origin, destination), group in grouped:

        route = f"{origin} -> {destination}"

        shipment_count = len(group)

        avg_delay_days = round(group["delay_days"].mean(), 1)

        total_revenue = round(group["cost_usd"].sum(), 2)

        # Carrier with the highest shipment count
        most_used_carrier = group["carrier"].value_counts().idxmax()

        route_summary.append(
            {
                "route": route,
                "shipment_count": shipment_count,
                "avg_delay_days": avg_delay_days,
                "total_revenue": total_revenue,
                "most_used_carrier": most_used_carrier,
            }
        )

    # Convert to DataFrame
    result = pd.DataFrame(route_summary)

    # Sort by shipment count (highest first)
    result = result.sort_values(
        by=["shipment_count","route"],
        ascending=[False, False]
    )

    # Return only top N routes
    result = result.head(top_n).reset_index(drop=True)

    return result


# TASK 2C
from datetime import date

def print_console_report(
    df: pd.DataFrame,
    carrier_kpis: pd.DataFrame,
    route_report: pd.DataFrame,
) -> None:
    """
    Print a formatted operations report to the console.
    """

    # Overall KPIs
    total_shipments = len(df)

    total_revenue = df["cost_usd"].sum()

    overall_otif = (
        (
            (df["status"] == "delivered")
            & (df["delay_days"] == 0)
        ).sum()
        / total_shipments
        * 100
    )

    avg_delay = df["delay_days"].mean()

    # Report Header

    print(
        f"\n=== AutoFinance Bank - Daily Shipment Report [{date.today()}] ==="
    )

    print(
        f"Total Shipments: {total_shipments} | "
        f"Total Revenue: ${total_revenue:,.2f} | "
        f"Overall OTIF: {overall_otif:.1f}% | "
        f"Avg Delay: {avg_delay:.1f} days"
    )

    # Carrier KPIs
    print("\n=== Carrier KPIs ===")

    print(
        f"{'Carrier':<10}"
        f"{'Shipments':>10}"
        f"{'Delivered':>12}"
        f"{'OTIF%':>10}"
        f"{'Avg Delay':>12}"
        f"{'Revenue':>12}"
    )

    for _, row in carrier_kpis.iterrows():

        print(
            f"{row['carrier']:<10}"
            f"{row['total_shipments']:>10}"
            f"{row['delivered']:>12}"
            f"{row['otif_pct']:>10.1f}"
            f"{row['avg_delay_days']:>12.1f}"
            f"${row['total_revenue']:>11.2f}"
        )

    # Route Report
    print("\n=== Top Routes ===")

    print(
        f"{'Route':<30}"
        f"{'Count':>8}"
        f"{'Avg Delay':>12}"
        f"{'Revenue':>12}"
    )

    for _, row in route_report.iterrows():

        print(
            f"{row['route']:<30}"
            f"{row['shipment_count']:>8}"
            f"{row['avg_delay_days']:>12.1f}"
            f"${row['total_revenue']:>11.2f}"
        )

    # Flagged Shipments
    flagged = df[df["delay_days"] > 3]

    print("\n=== Flagged Shipments (delay > 3 days) ===")

    if flagged.empty:
        print("None")
    else:
        for _, row in flagged.iterrows():
            print(
                f"{row['shipment_id']} "
                f"{row['carrier']} "
                f"{row['status']} "
                f"delay={int(row['delay_days'])} "
                f"cost=${row['cost_usd']:,.2f}"
            )


# TASK 3
def main() -> None:
    """
    Main entry point for the shipment reporting pipeline.
    """

    # Check if input file exists
    if not Path(INPUT_FILE).exists():
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        return

    # Load the CSV
    df = pd.read_csv(INPUT_FILE)

    # Required columns
    required_cols = {
        "shipment_id",
        "carrier",
        "status",
        "delay_days",
        "cost_usd",
    }

    # Check for missing columns
    missing_cols = required_cols - set(df.columns)

    if missing_cols:
        print(f"Error: Missing required columns: {sorted(missing_cols)}")
        return

    # Check if file is empty
    if len(df) == 0:
        print("Error: Input file contains no shipment data.")
        return

    # Compute reports
    carrier_kpis = compute_carrier_kpis(df)
    route_report = compute_route_report(df)

    # Save reports
    carrier_kpis.to_csv(SUMMARY_CSV, index=False)
    route_report.to_csv(ROUTES_CSV, index=False)

    print(f"Saved: {SUMMARY_CSV}")
    print(f"Saved: {ROUTES_CSV}")

    # Print console report
    print_console_report(
        df=df,
        carrier_kpis=carrier_kpis,
        route_report=route_report,
    )


if __name__ == "__main__":
    main()