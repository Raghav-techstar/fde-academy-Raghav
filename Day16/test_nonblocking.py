import time
import requests

BASE_URL = "http://127.0.0.1:8000"

# Time a POST to /analytics/refresh -- it should return in well under 1
# second even though refresh_analytics() takes 5 seconds internally.
start = time.time()
response = requests.post(f"{BASE_URL}/analytics/refresh")
elapsed = time.time() - start

print(f"POST returned in {elapsed:.2f}s (status {response.status_code})")
print(f"Response body: {response.json()}")
assert response.status_code == 202, "Expected 202 Accepted"
assert elapsed < 1.0, "POST took too long -- the task may be running synchronously, not in the background"

# Immediately GET /analytics/refresh-status -- state should still be
# 'running' or 'idle' momentarily, not yet 'complete'.
immediate_status = requests.get(f"{BASE_URL}/analytics/refresh-status").json()
print(f"\nImmediate status check: {immediate_status}")
assert immediate_status["state"] != "complete", "Refresh completed too fast -- background task may not be working"

# Wait 6 seconds, then GET /analytics/refresh-status again -- state should
# now be 'complete'.
print("\nWaiting 6 seconds for the background job to finish...")
time.sleep(6)

final_status = requests.get(f"{BASE_URL}/analytics/refresh-status").json()
print(f"Status after waiting: {final_status}")
assert final_status["state"] == "complete", "Refresh did not complete as expected"
assert final_status["last_run"] is not None, "last_run timestamp was not set"

print("\nAll checks passed: POST was non-blocking, and the background task completed.")