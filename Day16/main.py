"""
Day 16 - Exercise 1
Build a FastAPI Service with 5 Analytics Endpoints

Run:
    uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs in a browser and exercise all 5
endpoints through the Swagger UI, per Task 3's checklist.
"""

from datetime import date, datetime, timedelta

import jwt
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

app = FastAPI(title="TechStar Shipment Analytics API", version="1.0.0")

# ---------------------------------------------------------------------------
# Provided: in-memory dataset (stand-in for Day 12's PostgreSQL table)
# ---------------------------------------------------------------------------
shipments_db = [
    {"id": 1, "carrier": "BlueDart", "ship_date": date(2026, 6, 1), "freight_cost": 450.0, "status": "delivered"},
    {"id": 2, "carrier": "Delhivery", "ship_date": date(2026, 6, 2), "freight_cost": 620.0, "status": "in_transit"},
    {"id": 3, "carrier": "BlueDart", "ship_date": date(2026, 6, 3), "freight_cost": 310.0, "status": "delivered"},
]
next_id = 4


# =============================================================================
# Exercise 3: OAuth2 bearer token authentication
# =============================================================================

# ---------------------------------------------------------------------------
# Task 1: the token endpoint
# ---------------------------------------------------------------------------
# NOTE (per the exercise doc's own hint): this is a training simplification.
# A hardcoded secret and a single hardcoded demo user are NOT how you'd do
# this in production — a real deployment stores the secret outside source
# control (env var / secrets manager) and checks credentials against a real
# user store with hashed passwords.
SECRET_KEY = "training-only-secret-change-in-production"
ALGORITHM = "HS256"
DEMO_USER = {"username": "ops_admin", "password": "demo-password"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != DEMO_USER["username"] or form_data.password != DEMO_USER["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expire = datetime.utcnow() + timedelta(minutes=30)
    token = jwt.encode({"sub": form_data.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


# ---------------------------------------------------------------------------
# Task 2: the reusable authentication dependency
# ---------------------------------------------------------------------------
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise credentials_exception

    username = payload.get("sub")
    if username is None:
        raise credentials_exception

    return username


# ---------------------------------------------------------------------------
# Task 1: Pydantic models
# ---------------------------------------------------------------------------
class ShipmentCreate(BaseModel):
    carrier: str = Field(min_length=1)
    ship_date: date
    freight_cost: float = Field(gt=0)


class ShipmentResponse(BaseModel):
    id: int
    carrier: str
    ship_date: date
    freight_cost: float
    status: str


class AnalyticsSummary(BaseModel):
    total_shipments: int
    average_freight_cost: float
    status_counts: dict[str, int]


# ---------------------------------------------------------------------------
# Task 2: the 5 endpoints
# ---------------------------------------------------------------------------
def get_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": min(limit, 50)}


# ENDPOINT 1 (provided): list shipments with pagination and optional filter
@app.get("/shipments", response_model=list[ShipmentResponse])
def list_shipments(carrier: str | None = None, pagination=Depends(get_pagination)):
    results = shipments_db
    if carrier:
        results = [s for s in results if s["carrier"] == carrier]
    return results[pagination["skip"]:pagination["skip"] + pagination["limit"]]


# ENDPOINT 2: GET /shipments/{shipment_id}
@app.get("/shipments/{shipment_id}", response_model=ShipmentResponse)
def get_shipment(shipment_id: int):
    for shipment in shipments_db:
        if shipment["id"] == shipment_id:
            return shipment
    raise HTTPException(status_code=404, detail=f"Shipment {shipment_id} not found")


# ENDPOINT 3: POST /shipments (protected — creates data)
@app.post("/shipments", response_model=ShipmentResponse, status_code=201)
def create_shipment(shipment: ShipmentCreate, current_user: str = Depends(get_current_user)):
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


# ENDPOINT 4: GET /analytics/summary
@app.get("/analytics/summary", response_model=AnalyticsSummary)
def get_analytics_summary():
    total = len(shipments_db)
    average_cost = sum(s["freight_cost"] for s in shipments_db) / total if total else 0.0

    status_counts: dict[str, int] = {}
    for shipment in shipments_db:
        status_counts[shipment["status"]] = status_counts.get(shipment["status"], 0) + 1

    return {
        "total_shipments": total,
        "average_freight_cost": round(average_cost, 2),
        "status_counts": status_counts,
    }


# ENDPOINT 5: DELETE /shipments/{shipment_id} (protected — deletes data)
@app.delete("/shipments/{shipment_id}", status_code=204)
def delete_shipment(shipment_id: int, current_user: str = Depends(get_current_user)):
    for i, shipment in enumerate(shipments_db):
        if shipment["id"] == shipment_id:
            shipments_db.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Shipment {shipment_id} not found")


# ---------------------------------------------------------------------------
# Task 3: Protect the right endpoints — justification
# ---------------------------------------------------------------------------
# | Endpoint                  | Protect? | Justification                                          |
# |----------------------------|----------|--------------------------------------------------------|
# | GET /shipments             | No       | Read-only listing; the dashboard needs to query it      |
# |                            |          | freely, and it exposes no more than viewing shipments.  |
# | POST /shipments            | Yes      | Creates new data — must not be open to anyone on the    |
# |                            |          | network per the security review.                        |
# | DELETE /shipments/{id}     | Yes      | Destructive, irreversible — highest-risk endpoint here. |
# | POST /analytics/refresh    | Yes      | Triggers a background job that consumes server          |
# |                            |          | resources; an open trigger is a resource-exhaustion/DoS |
# |                            |          | risk even though it doesn't modify shipment records.     |
# | GET /analytics/summary     | No       | Read-only aggregate data, same reasoning as GET          |
# |                            |          | /shipments.                                              |
#
# GET /shipments/{shipment_id} (Endpoint 2, not listed in the doc's table)
# is left open too, for the same read-only reasoning.


# =============================================================================
# Exercise 2: Background task for async data processing
# =============================================================================

# ---------------------------------------------------------------------------
# Task 1: the simulated processing function + in-memory status tracker
# ---------------------------------------------------------------------------
import time

refresh_status = {"state": "idle", "last_run": None}


def refresh_analytics():
    """Simulates a slow nightly analytics refresh job. Runs in the
    background, AFTER the HTTP response for the request that triggered it
    has already been sent — the caller never waits for this to finish."""
    refresh_status["state"] = "running"

    time.sleep(5)  # simulate slow work (e.g. Day 12's cleaning pipeline)

    # Recompute something from shipments_db — the point is simulating real
    # work happening, not the specific computation.
    _ = len(shipments_db)
    _ = sum(s["freight_cost"] for s in shipments_db)

    refresh_status["state"] = "complete"
    refresh_status["last_run"] = datetime.now().isoformat()


# ---------------------------------------------------------------------------
# Task 2: wire the background task endpoint
# ---------------------------------------------------------------------------
@app.post("/analytics/refresh", status_code=202)
def trigger_refresh(background_tasks: BackgroundTasks, current_user: str = Depends(get_current_user)):
    background_tasks.add_task(refresh_analytics)
    return {"message": "Analytics refresh started in the background"}


@app.get("/analytics/refresh-status")
def get_refresh_status():
    return refresh_status