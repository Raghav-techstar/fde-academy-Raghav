from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional

# ============================================================
# TASK 1A: Carrier configuration using @dataclass
# ============================================================


@dataclass
class CarrierConfig:
    """Immutable carrier SLA configuration."""

    code: str
    name: str
    sla_days: int
    region: str
    active: bool = True

    def __post_init__(self) -> None:
        """
        Normalize the carrier code and validate SLA.
        """
        self.code = self.code.strip().upper()

        if self.sla_days <= 0:
            raise ValueError("sla_days must be greater than 0")


# ============================================================
# TASK 1B: ShipmentTracker class
# ============================================================


class ShipmentTracker:
    """
    Tracks a single shipment through its delivery lifecycle.

    Valid status transitions:

        pending     -> in_transit
        in_transit  -> delivered | exception
        exception   -> in_transit
        delivered   -> (terminal)

    """

    # Class attribute: valid transitions
    TRANSITIONS: dict[str, set[str]] = {
        "pending": {"in_transit"},
        "in_transit": {"delivered", "exception"},
        "exception": {"in_transit"},
        "delivered": set(),
    }

    PENALTY_RATE_PER_DAY: float = 150.0

    def __init__(
        self,
        shipment_id: str,
        carrier: CarrierConfig,
        origin: str,
        destination: str,
        delay_days: int = 0,
        cost_usd: float = 0.0,
    ) -> None:

        # Validate inputs
        if not shipment_id.strip():
            raise ValueError("shipment_id must not be empty")

        if origin == destination:
            raise ValueError("origin and destination must differ")

        self.shipment_id = shipment_id.strip().upper()
        self.carrier = carrier

        self.origin = origin.strip().title()
        self.destination = destination.strip().title()

        self.cost_usd = cost_usd

        self._delay_days = 0
        self.delay_days = delay_days

        self._status = "pending"

        self._history: list[tuple[str, str, datetime]] = []

    # ============================================================
    # TASK 1C: Properties
    # ============================================================

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, new_status: str) -> None:
        """
        Validate state transition and update shipment status.
        """

        if new_status not in self.TRANSITIONS:
            raise ValueError(f"Invalid status: {new_status}")

        if new_status not in self.TRANSITIONS[self._status]:
            allowed = self.TRANSITIONS[self._status]
            raise ValueError(
                f"Invalid transition: {self._status} -> {new_status}. "
                f"Allowed from '{self._status}': {allowed}"
            )
        self._history.append(
            (
                self._status,
                new_status,
                datetime.now(UTC),
            )
        )

        self._status = new_status

    @property
    def delay_days(self) -> int:
        """Return delay days."""
        return self._delay_days

    @delay_days.setter
    def delay_days(self, value: int) -> None:
        """Delay cannot be negative."""

        if value < 0:
            raise ValueError("delay_days cannot be negative")

        self._delay_days = value

    @property
    def is_delayed(self) -> bool:
        """True if shipment has any delay."""
        return self._delay_days > 0

    @property
    def breached_sla(self) -> bool:
        """True if shipment exceeded carrier SLA."""
        return self._delay_days > self.carrier.sla_days

    # ============================================================
    # TASK 1D: Methods
    # ============================================================

    def delay_penalty(
        self,
        rate: Optional[float] = None,
    ) -> float:
        """
        Return delay penalty in USD.
        """

        if rate is None:
            rate = self.PENALTY_RATE_PER_DAY

        return self.delay_days * rate

    def transition_to(
        self,
        new_status: str,
    ) -> None:
        """
        Public method to change shipment status.
        """

        self.status = new_status

    def status_history(self) -> list[str]:
        """
        Return readable status transition history.
        """

        history = []

        for old, new, timestamp in self._history:
            history.append(f"{old} -> {new} @ {timestamp.isoformat()}")

        return history

    def to_dict(self) -> dict:
        """
        Return a flat dictionary suitable for Foundry ingestion.
        """

        return {
            "shipment_id": self.shipment_id,
            "carrier_code": self.carrier.code,
            "carrier_name": self.carrier.name,
            "origin": self.origin,
            "destination": self.destination,
            "status": self.status,
            "delay_days": self.delay_days,
            "cost_usd": self.cost_usd,
            "penalty_usd": self.delay_penalty(),
            "is_delayed": self.is_delayed,
            "breached_sla": self.breached_sla,
            "transition_count": len(self._history),
        }

    def __repr__(self) -> str:
        return (
            f"ShipmentTracker("
            f"id={self.shipment_id}, "
            f"carrier={self.carrier.code}, "
            f"status={self.status}, "
            f"delay={self.delay_days}d)"
        )


if __name__ == "__main__":

    # --------------------------------------------------------
    # Define carriers
    # --------------------------------------------------------

    dhl = CarrierConfig(
        code="dhl",
        name="DHL Express",
        sla_days=2,
        region="APAC",
    )

    fedex = CarrierConfig(
        code="fedex",
        name="FedEx India",
        sla_days=3,
        region="APAC",
    )

    # --------------------------------------------------------
    # Create first shipment
    # --------------------------------------------------------

    s = ShipmentTracker(
        "sh-001",
        dhl,
        "Mumbai",
        "Delhi",
        delay_days=3,
        cost_usd=250.0,
    )

    print(s)

    # --------------------------------------------------------
    # Valid transitions
    # --------------------------------------------------------

    s.transition_to("in_transit")
    s.transition_to("delivered")

    print("History:", s.status_history())
    print(f"Penalty: ${s.delay_penalty()}")
    print("Breached SLA:", s.breached_sla)
    print("Foundry record:", s.to_dict())

    # --------------------------------------------------------
    # Invalid transition
    # --------------------------------------------------------

    try:
        s.transition_to("pending")
    except ValueError as e:
        print("Expected error:", e)

    # --------------------------------------------------------
    # Second shipment
    # --------------------------------------------------------

    s2 = ShipmentTracker(
        "sh-002",
        fedex,
        "Chennai",
        "Bangalore",
    )

    s2.transition_to("in_transit")
    s2.transition_to("exception")

    # Delayed at customs
    s2.delay_days = 2

    s2.transition_to("in_transit")
    s2.transition_to("delivered")

    print("\nS2 History:")

    for entry in s2.status_history():
        print(" ", entry)

    # --------------------------------------------------------
    # Batch summary
    # --------------------------------------------------------

    shipments = [
        s,
        s2,
        ShipmentTracker(
            "sh-003",
            dhl,
            "Pune",
            "Hyderabad",
            delay_days=0,
        ),
    ]

    records = [shipment.to_dict() for shipment in shipments]

    print(f"\nBatch: {len(records)} records ready for Foundry ingestion")

    delayed = [record for record in records if record["is_delayed"]]

    avg_penalty = sum(record["penalty_usd"] for record in delayed) / max(
        len(delayed), 1
    )

    print(f"Delayed: {len(delayed)} | Avg penalty: ${avg_penalty:.2f}")
