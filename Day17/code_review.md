# Day 17 - Exercise 3: Peer Code Review

## Review Target

Day 16 - TechStar Shipment Analytics API

## Review Type

Self-review using the Day 17 structured code review rubric.

---

############################################
## Task 1: Apply the Code Review Rubric
############################################

The Day 16 FastAPI service was reviewed across five dimensions:
Correctness, Readability, Test Coverage, Documentation, and Security.

| Dimension | Score / 5 | Evidence |
|---|---:|---|


| Correctness | 2/5 | The shipment models and most endpoints are implemented correctly, but the POST `/shipments` section currently uses `@app.get("/shipments")` and the function does not accept a `ShipmentCreate` parameter while still referencing `shipment.carrier`, `shipment.ship_date`, and `shipment.freight_cost`. This needs to be fixed before the service can be considered complete. |


| Readability | 4/5 | The code is organized into clear sections for authentication, models, endpoints, and background processing. Comments also explain the purpose of the main sections. Some functions and data structures could be made cleaner as the application grows. |


| Test Coverage | 3/5 | Authentication and background-task behaviour have dedicated verification scripts. However, there is no complete automated test suite covering all shipment CRUD operations, validation cases, analytics calculations, and error cases. |


| Documentation | 4/5 | The FastAPI application now has a proper title, description, version, endpoint summaries, and several endpoint docstrings. The documentation is much clearer, but the `GET /shipments` endpoint still needs its final docstring/summary update in the current version. |


| Security | 3/5 | Protected write operations use a reusable `get_current_user` dependency and JWT bearer authentication. However, the JWT secret and demo credentials are hardcoded in the source code, which is acceptable for training but must be changed for production. |

---

###########################################
## Task 2: Classify Findings by Severity
###########################################

### MUST FIX BEFORE MERGE

#### 1. Fix the POST `/shipments` endpoint

**Issue:**

The endpoint is currently declared as:

```python
@app.get("/shipments")
```

and the function is named `list_shipments`, but the code inside it tries
to create a new shipment using:

```python
shipment.carrier
shipment.ship_date
shipment.freight_cost
```

without receiving a `shipment: ShipmentCreate` parameter.

**Why it matters:**

The intended POST `/shipments` functionality will not work correctly. It
could also create a duplicate route definition for `GET /shipments`.

**Fix:**

Change it to a protected POST endpoint that accepts `ShipmentCreate`:

```python
@app.post(
    "/shipments",
    response_model=ShipmentResponse,
    status_code=201,
    summary="Create a shipment",
)
def create_shipment(
    shipment: ShipmentCreate,
    current_user: str = Depends(get_current_user),
):
    global next_id

    new_shipment = {
        "id": next_id,
        "carrier": shipment.carrier,
        "ship_date": shipment.ship_date,
        "freight_cost": shipment.freight_cost,
        "status": "pending",
    }

    shipments_db.append(new_shipment)
    next_id += 1

    return new_shipment
```

#### 2. Add automated tests for the main API behaviour

The current verification scripts cover authentication and the background
task, but the service would benefit from automated tests for:

- Creating a shipment
- Invalid freight cost
- Getting an unknown shipment
- Deleting a shipment
- Analytics calculations
- Pagination
- Carrier filtering

These tests would make future changes safer.

### CONSIDER FOR LATER

#### 1. Move the JWT secret outside the source code

The current implementation uses:

```python
SECRET_KEY = "training-only-secret-change-in-production"
```

This is acceptable for the training exercise, but a production system
should load the secret from an environment variable or secrets manager.

#### 2. Replace the in-memory shipment store

The service currently stores shipments in a Python list. A production
implementation should use a persistent database such as PostgreSQL.

This would also make the analytics queries more scalable for larger
datasets.

### DONE WELL

#### 1. Reusable authentication dependency

Using `get_current_user` keeps authentication logic in one place instead
of repeating token validation in every protected endpoint.

#### 2. Background refresh is non-blocking

The `/analytics/refresh` endpoint correctly uses FastAPI `BackgroundTasks`
and returns HTTP 202 while the refresh continues in the background.

#### 3. Pydantic validation

`ShipmentCreate` validates the carrier and ensures that `freight_cost` is
greater than zero:

```python
carrier: str = Field(min_length=1)
freight_cost: float = Field(gt=0)
```

#### 4. Appropriate HTTP status codes

The API uses:

- 201 for shipment creation
- 202 for starting the background refresh
- 204 for successful deletion
- 404 when a shipment cannot be found
- 401 for invalid authentication

---

##########################################
## Task 3: Response to Review Findings
##########################################

### MUST FIX Item 1

**Item:** Fix the POST `/shipments` endpoint.

**Response:** Agree, will fix.

**What I will change:**

I will change the route from `GET /shipments` to `POST /shipments`,
rename the function to `create_shipment`, add the `ShipmentCreate`
request parameter, and keep the authentication dependency so only
authenticated users can create shipments.

### MUST FIX Item 2

**Item:** Add automated tests for the main API behaviour.

**Response:** Agree, will fix.

**What I will change:**

I will add tests for shipment creation, validation failures, missing
shipments, deletion, analytics results, filtering, and pagination. This
will give better coverage than relying only on manual Swagger testing.

### CONSIDER FOR LATER Item 1

**Item:** Move the JWT secret outside the source code.

**Response:** Deferred, tracked for later.

**Reason:**

This is a training implementation, so the hardcoded secret is acceptable
for the exercise. Before production deployment, it should be moved to an
environment variable or secrets manager.

### CONSIDER FOR LATER Item 2

**Item:** Replace the in-memory shipment store with PostgreSQL.

**Response:** Deferred, tracked for later.

**Reason:**

The current exercise intentionally uses an in-memory dataset. PostgreSQL
would be more appropriate when persistence, larger datasets, concurrent
access, and production deployment are required.