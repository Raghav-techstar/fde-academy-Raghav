import pandas as pd

# TASK 1
API_RESPONSE = {
    "meta": {
        "request_id": "REQ-2024-001",
        "total_records": 3,
        "page": 1,
    },
    "shipments": [
        {
            # SH-001
            "id": "SH-001",
            "reference": "PO-AFB-2024-441",

            "status": {
                "code": "IN_TRANSIT",
                "description": "Package in transit to destination hub",
                "updated_at": "2024-01-20T08:15:00Z",
            },

            "carrier": {
                "name": "DHL Express",
                "code": "DHL",
                "service_type": "EXPRESS",
                "contact": {
                    "email": "ops@dhl.in",
                    "phone": "+91-22-12345678",
                },
            },

            "route": {
                "origin": {
                    "city": "Mumbai",
                    "state": "MH",
                    "pin": "400001",
                },
                "destination": {
                    "city": "Delhi",
                    "state": "DL",
                    "pin": "110001",
                },
                "estimated_delivery": "2024-01-22",
                "distance_km": 1450,
            },

            "events": [
                {
                    "ts": "2024-01-18T10:00:00Z",
                    "location": "Mumbai Warehouse",
                    "type": "PICKUP",
                },
                {
                    "ts": "2024-01-19T06:30:00Z",
                    "location": "Nagpur Hub",
                    "type": "IN_TRANSIT",
                },
                {
                    "ts": "2024-01-20T08:15:00Z",
                    "location": "Delhi Hub",
                    "type": "ARRIVED",
                },
            ],

            "charges": {
                "base": 850.0,
                "fuel_surcharge": 127.5,
                "gst": 177.75,
                "total": 1155.25,
            },

            "delay_days": 0,
        },
        {
            # SH-002
            "id": "SH-002",
            "reference": "PO-AFB-2024-442",

            "status": {
                "code": "DELAYED",
                "description": "Delayed due to customs clearance",
                "updated_at": "2024-01-20T07:00:00Z",
            },

            "carrier": {
                "name": "FedEx India",
                "code": "FEDEX",
                "service_type": "STANDARD",
                "contact": {
                    "email": "support@fedex.in"
                },
            },

            "route": {
                "origin": {
                    "city": "Chennai",
                    "state": "TN",
                    "pin": "600001",
                },
                "destination": {
                    "city": "Bangalore",
                    "state": "KA",
                    "pin": "560001",
                },
                "estimated_delivery": "2024-01-21",
                "distance_km": 346,
            },

            "events": [
                {
                    "ts": "2024-01-18T14:00:00Z",
                    "location": "Chennai Port",
                    "type": "PICKUP",
                },
                {
                    "ts": "2024-01-20T07:00:00Z",
                    "location": "Customs Delhi",
                    "type": "HELD",
                },
            ],

            "charges": {
                "base": 320.0,
                "fuel_surcharge": 48.0,
                "gst": 66.24,
                "total": 434.24,
            },

            "delay_days": 3,
        },

        {
            # SH-003
            "id": "SH-003",
            "reference": None,

            "status": {
                "code": "DELIVERED",
                "updated_at": "2024-01-19T16:00:00Z",
            },

            "carrier": {
                "name": "BlueDart",
                "code": "BLUEDART",
                "service_type": "ECONOMY",
            },

            "route": {
                "origin": {
                    "city": "Pune",
                },
                "destination": {
                    "city": "Hyderabad",
                    "state": "TS",
                    "pin": "500001",
                },
                "estimated_delivery": "2024-01-19",
                "distance_km": 559,
            },

            "events": [
                {
                    "ts": "2024-01-17T09:00:00Z",
                    "location": "Pune Depot",
                    "type": "PICKUP",
                },
                {
                    "ts": "2024-01-19T16:00:00Z",
                    "location": "Hyderabad Depot",
                    "type": "DELIVERED",
                },
            ],

            "charges": {
                "base": 180.0,
                "gst": 32.4,
                "total": 212.4,
            },

            "delay_days": 0,
        },
    ],
}




# TASK 2A
def extract_shipment_record(shipment: dict) -> dict:
    """
    Flatten a single shipment dictionary into a flat record.

    Missing nested fields should return None instead of raising KeyError.
    """

    # Nested dictionaries
    status = shipment.get("status", {})
    carrier = shipment.get("carrier", {})
    route = shipment.get("route", {})
    origin = route.get("origin", {})
    destination = route.get("destination", {})
    charges = shipment.get("charges", {})

    # Events
    events = shipment.get("events", [])

    event_count = len(events)

    if event_count > 0:
        latest_event = events[-1]
        latest_event_type = latest_event.get("type")
        latest_event_location = latest_event.get("location")
    else:
        latest_event_type = None
        latest_event_location = None

    # Return flattened record
    return {
        "shipment_id": shipment.get("id"),
        "reference": shipment.get("reference"),

        "status_code": status.get("code"),
        "status_desc": status.get("description"),

        "carrier_name": carrier.get("name"),
        "carrier_code": carrier.get("code"),
        "service_type": carrier.get("service_type"),
        "carrier_email": carrier.get("contact", {}).get("email"),

        "origin_city": origin.get("city"),
        "origin_state": origin.get("state"),

        "dest_city": destination.get("city"),
        "dest_state": destination.get("state"),

        "est_delivery": route.get("estimated_delivery"),
        "distance_km": route.get("distance_km"),

        "event_count": event_count,
        "latest_event_type": latest_event_type,
        "latest_event_loc": latest_event_location,

        "charge_base": charges.get("base"),
        "charge_gst": charges.get("gst"),
        "charge_total": charges.get("total"),

        "delay_days": shipment.get("delay_days", 0),
    }


# TASK 2B
def parse_api_response(response: dict) -> list[dict]:
    """
    Extract all shipment records from the full API response.

    Args:
        response: The complete API response dictionary.

    Returns:
        List of flattened shipment records.
        Returns an empty list if the "shipments" key is missing.
    """

    shipments = response.get("shipments", [])

    return [extract_shipment_record(shipment) for shipment in shipments]


# TASK 2C
def compute_carrier_summary(records: list[dict]) -> list[dict]:
    """
    Group shipment records by carrier_code and compute summary statistics.

    Returns:
        List of dictionaries, one per carrier,
        sorted by total_revenue in descending order.
    """

    carrier_stats = {}

    for record in records:

        carrier_code = record.get("carrier_code")
        carrier_name = record.get("carrier_name")

        if carrier_code not in carrier_stats:
            carrier_stats[carrier_code] = {
                "carrier_code": carrier_code,
                "carrier_name": carrier_name,
                "shipment_count": 0,
                "total_revenue": 0.0,
                "delayed_count": 0,
                "delay_sum": 0,
                "delay_count": 0,
            }

        stats = carrier_stats[carrier_code]

        # Shipment count
        stats["shipment_count"] += 1  # type: ignore

        # Revenue
        revenue = record.get("charge_total")
        if revenue is not None:
            stats["total_revenue"] += revenue  # type: ignore

        # Delay statistics
        delay = record.get("delay_days")

        if delay is not None:
            stats["delay_sum"] += delay  # type: ignore
            stats["delay_count"] += 1  # type: ignore

            if delay > 0:
                stats["delayed_count"] += 1  # type: ignore

    summary = []

    for stats in carrier_stats.values():

        delay_count = int(stats["delay_count"]) # type: ignore[arg-type]
        delay_sum = float(stats["delay_sum"]) # type: ignore[arg-type]

        if delay_count > 0:
            avg_delay = round(delay_sum / delay_count, 1)
        else:
            avg_delay = 0.0

        summary.append(
            {
                "carrier_code": stats["carrier_code"],
                "carrier_name": stats["carrier_name"],
                "shipment_count": int(stats["shipment_count"]), # type: ignore[arg-type]
                "total_revenue": round(float(stats["total_revenue"]), 2), # type: ignore[arg-type]
                "delayed_count": int(stats["delayed_count"]), # type: ignore[arg-type]
                "avg_delay_days": avg_delay,
            }
        )

    # Sort by total revenue (highest first)
    summary.sort(
        key=lambda row: float(row["total_revenue"]),  # type: ignore[arg-type]
        reverse=True,
    )

    return summary




if __name__ == "__main__":

    records = parse_api_response(API_RESPONSE)

    print(f"Parsed {len(records)} shipment records")

    # Save CSV
    df = pd.DataFrame(records)
    df.to_csv("shipments_parsed.csv", index=False)
    print("Saved: shipments_parsed.csv")

    # Carrier summary
    summary = compute_carrier_summary(records)

    print("\n=== Carrier Summary ===")

    for row in summary:
        print(
            f"{row['carrier_name']:<15} "
            f"shipments={row['shipment_count']} "
            f"revenue={row['total_revenue']:,.2f} "
            f"delayed={row['delayed_count']} "
            f"avg_delay={row['avg_delay_days']}d"
        )