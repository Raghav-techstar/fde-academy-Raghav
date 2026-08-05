########################
# TASK - 1
########################
import os
import json

from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("API KEY")
)

test_notes = [

    "On 03/14, Pump 4 began showing elevated vibration during the morning shift. Technician flagged for inspection within 48 hours - not an immediate safety concern.",

    "URGENT - Tank 3 emergency shutoff valve failed during routine test this morning. Line supervisor notified immediately.",

    "Filter replacement on HVAC unit 2 completed, no issues.",

    "Conveyor belt 12 motor showing signs of overheating, exact date of onset unclear, reported by night shift.",

    "Compressor unit 7 pressure readings inconsistent since last Tuesday, monitoring closely, no action taken yet."
]

baseline_prompt = """
Extract the following information from the maintenance report.

Return:

- equipment_id
- issue_type
- severity
- reported_date

Maintenance Report:

{note}
"""

baseline_results = []

print("=" * 80)
print("TASK 1 - BASELINE EXTRACTION")
print("=" * 80)

for note in test_notes:

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=250,
        messages=[
            {
                "role": "user",
                "content": baseline_prompt.format(note=note)
            }
        ]
    )

    output = ""

    for block in response.content:
        if getattr(block, "type", "") == "text":
            output += block.text

    output = output.strip()

    print("\nNOTE")
    print(note)

    print("\nOUTPUT")
    print(output)

    print("-" * 80)

    baseline_results.append(output)


########################################
# TASK - 2
########################################

improved_prompt = """
You are an AI assistant that extracts structured information from maintenance reports.

Return ONLY valid JSON using the following schema:

{{
    "equipment_id": "string",
    "issue_type": "string",
    "severity": "low | medium | high",
    "reported_date": "string | null"
}}

Rules:
- severity must be exactly one of: low, medium, high.
- If the report does not contain a date, use null.
- Do not include any explanation or extra text.
- Return only the JSON object.

Example 1

Maintenance Report:
Generator 5 failed during startup on 05/20. Immediate repair required.

Output:
{{
    "equipment_id": "Generator 5",
    "issue_type": "Startup failure",
    "severity": "high",
    "reported_date": "05/20"
}}

Example 2

Maintenance Report:
Cooling fan 2 inspected yesterday. Minor dust buildup observed. Cleaning scheduled.

Output:
{{
    "equipment_id": "Cooling fan 2",
    "issue_type": "Dust buildup",
    "severity": "low",
    "reported_date": null
}}

Maintenance Report:

{note}
"""

improved_results = []

print("\n")
print("=" * 80)
print("TASK 2 - IMPROVED EXTRACTION")
print("=" * 80)

for note in test_notes:

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=250,
        messages=[
            {
                "role": "user",
                "content": improved_prompt.format(note=note)
            }
        ]
    )

    output = ""

    for block in response.content:
        if getattr(block, "type", "") == "text":
            output += block.text

    output = output.strip()

    print("\nNOTE")
    print(note)

    print("\nOUTPUT")
    print(output)

    print("-" * 80)

    improved_results.append(output)


#######################################
# TASK - 3
#######################################

def validate_extraction(raw_response):

    try:
        # Remove Markdown code fences if present
        raw_response = raw_response.strip()

        if raw_response.startswith("```json"):
            raw_response = raw_response.replace("```json", "", 1)

        if raw_response.endswith("```"):
            raw_response = raw_response[:-3]

        raw_response = raw_response.strip()

        data = json.loads(raw_response)

    except Exception as e:
        return False, f"Invalid JSON: {e}"

    required_fields = [
        "equipment_id",
        "issue_type",
        "severity",
        "reported_date",
    ]

    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"

    if data["severity"] not in [
        "low",
        "medium",
        "high",
    ]:
        return False, "Invalid severity value"

    return True, data

# validating task 1 outputs
print()
print("=" * 80)
print("TASK 3 - VALIDATING BASELINE OUTPUTS")
print("=" * 80)

baseline_success = 0

for index, output in enumerate(baseline_results, start=1):

    valid, result = validate_extraction(output)

    print(f"Note {index}")

    if valid:
        print("PASS")
        baseline_success += 1
    else:
        print("FAIL")
        print(result)

    print("-" * 60)

# validating task 2 outputs
print()
print("=" * 80)
print("TASK 3 - VALIDATING IMPROVED OUTPUTS")
print("=" * 80)

improved_success = 0

for index, output in enumerate(improved_results, start=1):

    valid, result = validate_extraction(output)

    print(f"Note {index}")

    if valid:
        print("PASS")
        improved_success += 1
    else:
        print("FAIL")
        print(result)

    print("-" * 60)

# printing success rates
print()
print("=" * 80)
print("FINAL COMPARISON")
print("=" * 80)

print(f"Baseline (Task 1) success rate : {baseline_success} / {len(test_notes)}")

print(f"Improved (Task 2) success rate : {improved_success} / {len(test_notes)}")