####################################
# TASK - 1
####################################


from __future__ import annotations

from datetime import UTC, datetime
from typing import Optional, cast

from fastapi import FastAPI, HTTPException, Query, Depends, Header
from pydantic import BaseModel, Field, field_validator

import asyncio
import random

app = FastAPI(
    title="TechStar Group - Supply Chain Status API",
    description=(
        "Internal utility API for AutoFinance Bank discovery "
        "phase 1 data validation. Built by FDE Academy Cohort."
    ),
    version="1.0.0",
)


# ============================================================
# MOCK IN-MEMORY DATABASE
# ============================================================

MOCK_SHIPMENTS: dict[str, dict] = {
    "SH001": {
        "shipment_id": "SH001",
        "carrier": "DHL",
        "status": "in_transit",
        "origin": "Mumbai",
        "destination": "Delhi",
        "cost_usd": 250.0,
        "created_at": "2024-01-18T10:00:00",
    },
    "SH002": {
        "shipment_id": "SH002",
        "carrier": "FEDEX",
        "status": "delivered",
        "origin": "Chennai",
        "destination": "Bangalore",
        "cost_usd": 180.5,
        "created_at": "2024-01-17T09:30:00",
    },
    "SH003": {
        "shipment_id": "SH003",
        "carrier": "BLUEDART",
        "status": "delayed",
        "origin": "Pune",
        "destination": "Hyderabad",
        "cost_usd": 320.0,
        "created_at": "2024-01-16T14:15:00",
    },
}


MOCK_CARRIERS: dict[str, dict] = {
    "DHL": {
        "code": "DHL",
        "name": "DHL Express",
        "sla_days": 2,
    },
    "FEDEX": {
        "code": "FEDEX",
        "name": "FedEx India",
        "sla_days": 3,
    },
    "BLUEDART": {
        "code": "BLUEDART",
        "name": "BlueDart",
        "sla_days": 2,
    },
}

VALID_API_KEYS = {
    "techstar-fde-key-001",
    "techstar-fde-key-002",
}


def verify_api_key(
    x_api_key: Optional[str] = Header(default=None),
) -> str:
    """
    Validates the X-API-Key header.
    Raises 401 if missing.
    Raises 403 if invalid.
    """

    if x_api_key is None:
        raise HTTPException(
            status_code=401,
            detail="X-API-Key header missing",
        )

    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key",
        )

    return x_api_key


######################################
# TASK - 2
######################################
# ============================================================
# RESPONSE MODELS
# ============================================================


class ShipmentResponse(BaseModel):
    """What every shipment endpoint returns."""

    shipment_id: str
    carrier: str
    status: str
    origin: str
    destination: str
    cost_usd: float
    created_at: str


class CarrierResponse(BaseModel):
    code: str
    name: str
    sla_days: int


# ============================================================
# REQUEST MODEL
# ============================================================


class ShipmentCreateRequest(BaseModel):
    """Validates the body of POST /shipments."""

    shipment_id: str = Field(..., min_length=3, max_length=20)
    carrier: str = Field(..., min_length=2)
    origin: str = Field(..., min_length=2)
    destination: str = Field(..., min_length=2)
    cost_usd: float = Field(..., gt=0)

    @field_validator("carrier")
    @classmethod
    def validate_carrier(cls, value: str) -> str:
        value = value.upper()

        if value not in {"DHL", "FEDEX", "BLUEDART"}:
            raise ValueError("Carrier must be one of: DHL, FEDEX, BLUEDART")

        return value


################################
# TASK - 3
# 3 A
################################
@app.get("/shipments", response_model=list[ShipmentResponse])
def list_shipments(
    status: Optional[str] = None,
    carrier: Optional[str] = None,
    api_key: str = Depends(verify_api_key),
) -> list[dict]:
    """
    GET /shipments
    GET /shipments?status=delayed
    GET /shipments?carrier=DHL&status=in_transit
    """

    shipments = list(MOCK_SHIPMENTS.values())

    if status:
        shipments = [shipment for shipment in shipments if shipment["status"] == status]

    if carrier:
        shipments = [
            shipment
            for shipment in shipments
            if shipment["carrier"].upper() == carrier.upper()
        ]

    return shipments


################################
# TASK - 3 B
################################
@app.get("/shipments/{shipment_id}", response_model=ShipmentResponse)
def get_shipment(
    shipment_id: str,
    api_key: str = Depends(verify_api_key),
) -> dict:
    """GET /shipments/SH001"""

    if shipment_id not in MOCK_SHIPMENTS:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found",
        )

    return MOCK_SHIPMENTS[shipment_id]


################################
# TASK - 3 C
################################
@app.post(
    "/shipments",
    response_model=ShipmentResponse,
    status_code=201,
)
def create_shipment(
    payload: ShipmentCreateRequest,
    api_key: str = Depends(verify_api_key),
) -> dict:
    if payload.shipment_id in MOCK_SHIPMENTS:
        raise HTTPException(
            status_code=409,
            detail="Shipment already exists",
        )

    shipment = payload.model_dump()

    shipment["status"] = "pending"
    shipment["created_at"] = datetime.now(UTC).isoformat()

    MOCK_SHIPMENTS[payload.shipment_id] = shipment

    return shipment


################################
# TASK - 3 D
################################
@app.get("/carriers", response_model=list[CarrierResponse])
def list_carriers(
    api_key: str = Depends(verify_api_key),
) -> list[dict]:
    """GET /carriers"""

    return list(MOCK_CARRIERS.values())


@app.get("/")
def home():
    return {
        "message": "TechStar Group - Supply Chain Status API",
        "docs": "/docs",
    }


#################################
# EXRECISE - 2
#################################
# TASK - 1

# ============================================================
# PROVIDED: 3 vendor simulators with DIFFERENT response shapes
# ============================================================


async def call_vendor_a(shipment_id: str) -> dict:
    """Vendor A: clean field names, occasionally slow."""
    await asyncio.sleep(0.1)

    return {
        "id": shipment_id,
        "current_status": "in_transit",
        "eta_days": 2,
    }


async def call_vendor_b(shipment_id: str) -> dict:
    """Vendor B: different field names, occasionally raises an error."""
    await asyncio.sleep(0.15)

    # Simulates ~30% failure rate
    if random.random() < 0.3:
        raise ConnectionError("Vendor B timeout")

    return {
        "shipmentRef": shipment_id,
        "trackingState": "DELAYED",
        "delayHrs": 36,
    }


async def call_vendor_c(shipment_id: str) -> dict:
    """Vendor C: nested response shape, reliable."""
    await asyncio.sleep(0.08)

    return {
        "shipment": {
            "identifier": shipment_id,
            "state": {
                "code": "DELIVERED",
                "confidence": 0.95,
            },
        },
    }


####################################
# TASK - 2 A
###################################
# ============================================================
# Unified model
# ============================================================


class VendorStatus(BaseModel):
    """Unified shape — every vendor response gets normalised to this."""

    shipment_id: str
    source_vendor: str
    normalised_status: str
    raw: dict


# TASK 2A: Normaliser functions


def normalise_vendor_a(raw: dict) -> VendorStatus:
    return VendorStatus(
        shipment_id=raw["id"],
        source_vendor="vendor_a",
        normalised_status=raw.get("current_status", "unknown"),
        raw=raw,
    )


def normalise_vendor_b(raw: dict) -> VendorStatus:
    """
    Vendor B uses 'shipmentRef' and 'trackingState' (UPPER_CASE values).
    """

    status_map = {
        "DELAYED": "delayed",
        "DELIVERED": "delivered",
        "IN_TRANSIT": "in_transit",
    }

    return VendorStatus(
        shipment_id=raw["shipmentRef"],
        source_vendor="vendor_b",
        normalised_status=status_map.get(
            raw.get("trackingState", ""),
            "unknown",
        ),
        raw=raw,
    )


def normalise_vendor_c(raw: dict) -> VendorStatus:
    """
    Vendor C nests everything under raw['shipment']['state']['code'].
    """

    shipment = raw.get("shipment", {})
    state = shipment.get("state", {})

    status_map = {
        "DELAYED": "delayed",
        "DELIVERED": "delivered",
        "IN_TRANSIT": "in_transit",
    }

    return VendorStatus(
        shipment_id=shipment.get("identifier", ""),
        source_vendor="vendor_c",
        normalised_status=status_map.get(
            state.get("code", ""),
            "unknown",
        ),
        raw=raw,
    )


#####################################
# TASK - 2 B
#####################################
@app.get(
    "/supply-chain-status/{shipment_id}",
    response_model=list[VendorStatus],
)
async def get_supply_chain_status(
    shipment_id: str,
    api_key: str = Depends(verify_api_key),
) -> list[VendorStatus]:

    results = await asyncio.gather(
        call_vendor_a(shipment_id),
        call_vendor_b(shipment_id),
        call_vendor_c(shipment_id),
        return_exceptions=True,
    )

    normalisers = [
        normalise_vendor_a,
        normalise_vendor_b,
        normalise_vendor_c,
    ]

    final_results = []

    for result, normaliser in zip(results, normalisers):
        if isinstance(result, Exception):
            continue
        result = cast(dict, result)
        final_results.append(normaliser(result))

    if not final_results:
        raise HTTPException(
            status_code=503,
            detail="All vendor systems unreachable",
        )

    return final_results
