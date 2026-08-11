"""
Day 16 - Exercise 3
Verify Authentication Behaviour

Run this AFTER starting the server (uvicorn main:app --reload) in a
SEPARATE terminal.

Run:
    python test_auth.py
"""

import requests

BASE_URL = "http://127.0.0.1:8000"

# ---------------------------------------------------------------------------
# 1. POST /token with correct credentials -> should return a valid bearer token
# ---------------------------------------------------------------------------
response = requests.post(
    f"{BASE_URL}/token",
    data={"username": "ops_admin", "password": "demo-password"},
)
print(f"POST /token (correct creds): {response.status_code}")
assert response.status_code == 200, "Expected 200 for correct credentials"
token_data = response.json()
print(f"  {token_data}")
assert "access_token" in token_data and token_data["token_type"] == "bearer"

token = token_data["access_token"]

# ---------------------------------------------------------------------------
# 2. POST /token with WRONG credentials -> should be rejected
# ---------------------------------------------------------------------------
bad_response = requests.post(
    f"{BASE_URL}/token",
    data={"username": "ops_admin", "password": "wrong-password"},
)
print(f"\nPOST /token (wrong creds): {bad_response.status_code}")
assert bad_response.status_code == 401, "Expected 401 for incorrect credentials"

# ---------------------------------------------------------------------------
# 3. Call a protected endpoint WITHOUT a token -> should return 401
# ---------------------------------------------------------------------------
no_token_response = requests.post(
    f"{BASE_URL}/shipments",
    json={"carrier": "FedEx", "ship_date": "2026-06-10", "freight_cost": 275.5},
)
print(f"\nPOST /shipments (no token): {no_token_response.status_code}")
assert no_token_response.status_code == 401, "Expected 401 without a token"

# ---------------------------------------------------------------------------
# 4. Call a protected endpoint with an INVALID token -> should return 401
# ---------------------------------------------------------------------------
bad_token_response = requests.post(
    f"{BASE_URL}/shipments",
    json={"carrier": "FedEx", "ship_date": "2026-06-10", "freight_cost": 275.5},
    headers={"Authorization": "Bearer not-a-real-token"},
)
print(f"POST /shipments (invalid token): {bad_token_response.status_code}")
assert bad_token_response.status_code == 401, "Expected 401 for an invalid token"

# ---------------------------------------------------------------------------
# 5. Call a protected endpoint WITH a valid token -> should succeed
# ---------------------------------------------------------------------------
good_response = requests.post(
    f"{BASE_URL}/shipments",
    json={"carrier": "FedEx", "ship_date": "2026-06-10", "freight_cost": 275.5},
    headers={"Authorization": f"Bearer {token}"},
)
print(f"\nPOST /shipments (valid token): {good_response.status_code}")
assert good_response.status_code == 201, "Expected 201 with a valid token"
print(f"  Created: {good_response.json()}")

# ---------------------------------------------------------------------------
# 6. Read-only endpoint should work with NO token at all
# ---------------------------------------------------------------------------
read_response = requests.get(f"{BASE_URL}/shipments")
print(f"\nGET /shipments (no token, read-only): {read_response.status_code}")
assert read_response.status_code == 200, "Read-only endpoint should not require auth"

print("\nAll checks passed: login works, 401s are correct, and valid-token access succeeds.")