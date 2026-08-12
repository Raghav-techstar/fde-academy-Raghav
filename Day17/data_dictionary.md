# ShipmentResponse Data Dictionary

**DATA DICTIONARY:** ShipmentResponse

**SOURCE:** GET /shipments, GET /shipments/{shipment_id}, POST /shipments

**OWNER:** FDE / Operations Team

**LAST UPDATED:** 2026-08-12

| Field | Type | Nullable | Description | Example |
|---|---|---|---|---|
| id | integer | No | Unique identifier assigned to the shipment | 1 |
| carrier | string | No | Name of the shipping carrier | BlueDart |
| ship_date | date | No | Date associated with the shipment | 2026-06-01 |
| freight_cost | float | No | Freight cost of the shipment | 450.0 |
| status | string | No | Current status of the shipment | delivered |

## Known Limitations

- Shipment data is stored in memory.
- Data is lost when the application restarts.
- Analytics are calculated from the current in-memory dataset.
- The authentication currently uses a demo user for training purposes.
- The JWT secret is currently stored in the source code and should be moved to a secure environment variable or secrets manager in production.