# TechStar Shipment Analytics API

## Overview

The TechStar Shipment Analytics API is a FastAPI service for managing
shipment records and providing shipment analytics for an operations
dashboard.

The service also supports asynchronous analytics refresh and OAuth2
bearer-token authentication for protected operations.

## Setup

The API is currently implemented in the `Day16` directory.

Navigate to the Day16 directory:

```powershell
cd ..\Day16
```

Create a virtual environment if required:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```powershell
pip install -r requirements.txt
```

## Running Locally

From the Day16 directory, start the API with:

```powershell
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive Swagger documentation is available at:

```
http://127.0.0.1:8000/docs
```

## Authentication

The API uses OAuth2 bearer-token authentication for protected operations.

### Obtain a Token

Send a POST request to:

```
POST /token
```

Use the following training credentials:

| Field | Value |
|---|---|
| Username | `ops_admin` |
| Password | `demo-password` |

The response contains an access token.

Use the returned token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Protected Endpoints

The following endpoints require a valid bearer token:

- `POST /shipments`
- `DELETE /shipments/{shipment_id}`
- `POST /analytics/refresh`

### Read-Only Endpoints

The following endpoints are currently available without authentication:

- `GET /shipments`
- `GET /shipments/{shipment_id}`
- `GET /analytics/summary`
- `GET /analytics/refresh-status`

This authentication setup is intended for the training implementation.
A production system should use a proper user store and securely managed
secrets.

## Key Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/token` | Authenticate and obtain a JWT bearer token |
| GET | `/shipments` | List shipments with optional carrier filtering and pagination |
| GET | `/shipments/{shipment_id}` | Retrieve a specific shipment |
| POST | `/shipments` | Create a new shipment |
| DELETE | `/shipments/{shipment_id}` | Delete an existing shipment |
| GET | `/analytics/summary` | Retrieve aggregated shipment analytics |
| POST | `/analytics/refresh` | Start an asynchronous analytics refresh |
| GET | `/analytics/refresh-status` | Check the current refresh status |

## Shipment Operations

### List Shipments

```
GET /shipments
```

Returns shipment records.

Optional query parameters can be used for:

- Carrier filtering
- Pagination

Example:

```
GET /shipments?carrier=FedEx&skip=0&limit=10
```

### Get a Shipment

```
GET /shipments/{shipment_id}
```

Returns a shipment using its unique ID.

### Create a Shipment

```
POST /shipments
```

Requires authentication.

Example request body:

```json
{
  "carrier": "FedEx",
  "ship_date": "2026-06-10",
  "freight_cost": 275.5
}
```

The API generates the shipment ID and initially assigns the shipment
a `pending` status.

### Delete a Shipment

```
DELETE /shipments/{shipment_id}
```

Requires authentication.

Deletes the shipment associated with the supplied ID.

## Analytics

### Analytics Summary

```
GET /analytics/summary
```

Returns aggregated information from the current shipment dataset,
including shipment counts and freight-cost information.

### Start Analytics Refresh

```
POST /analytics/refresh
```

Requires authentication.

The refresh operation runs as a background task. The endpoint returns
HTTP 202 Accepted without waiting for the refresh to finish.

### Check Refresh Status

```
GET /analytics/refresh-status
```

Returns the current state of the analytics refresh and the timestamp
of the most recent completed refresh.

## Data Storage

The current implementation stores shipment records in an in-memory
Python list.

This means:

- Data is lost when the application restarts.
- The service does not currently use a persistent database.
- Analytics are calculated from the current in-memory shipment data.
- The refresh status is also stored in memory.

## API Documentation

When the server is running, complete interactive API documentation
is available through Swagger UI:

```
http://127.0.0.1:8000/docs
```

The OpenAPI schema is also available at:

```
http://127.0.0.1:8000/openapi.json
```

## Known Limitations

- Shipment data is stored only in memory.
- Data is lost when the application restarts.
- The analytics refresh status is stored in memory.
- Background tasks may be lost if the application process stops
  before the task completes.
- The authentication implementation uses demo credentials for training.
- The JWT secret should be stored securely outside the source code
  in a production environment.
- The current implementation is intended for a training/demo
  environment rather than production use.

## Related Documentation

- [ADR-001](./ADR-001.md)
- [ShipmentResponse Data Dictionary](./data_dictionary.md)