#                           STYLE - 1 (ZERO-SHOT)

# Classify the urgency of this maintenance note as LOW, MEDIUM, or HIGH.


#                           STYLE - 2 (ROLE-BASED)

# You are a senior plant safety coordinator responsible for ensuring worker safety
# and preventing equipment failures.Analyze the maintenance note below and classify
# its urgency as LOW, MEDIUM, or HIGH.


#                           STYLE - 3 (FEW-SHOT)

#Classify the urgency of maintenance notes as LOW, MEDIUM, or HIGH.
#Example 1
#Maintenance Note:
#Backup generator tested successfully. No faults detected.
#Urgency:
#LOW
#Example 2
#Maintenance Note:
#Boiler pressure valve stuck, steam leaking near control panel. Area evacuated.
#Urgency:
#HIGH
#Now classify this maintenance note.


#                           STYLE - 4 (CHAIN-OF-THOUGHT)

# Think through the following:
#1. What equipment is affected?
#2. Is there any immediate safety risk?
#3. Will operations be affected?
#4. Does this require urgent action?

#Finally, classify the urgency as one of:

#LOW
#MEDIUM
#HIGH

#                          STYLE - 5 (STRUCTURED OUTPUT)

# You are a maintenance operations assistant.
#Classify the urgency of the maintenance note.
#Return ONLY valid JSON.
#Format:
#{
 # "urgency": "LOW | MEDIUM | HIGH",
 # "reason": "One sentence explaining the classification."
#}



###########################
# TASK - 2
###########################
import os
import json
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("API KEY")   # Change to ANTHROPIC_API_KEY if needed
)

# Test maintenance notes
test_notes = [
    "Pump 4 vibration levels remain within normal range after service.",
    "Conveyor belt 12 motor overheating, smoke smell reported, line stopped.",
    "Compressor unit 7 pressure gauge reading slightly inconsistent, monitoring.",
    "Emergency shutoff valve on Tank 3 failed to engage during test.",
    "Routine filter replacement completed on HVAC unit 2, no issues found."
]

# Prompt styles
styles = {

    "Zero Shot": """
Classify the urgency of this maintenance note as LOW, MEDIUM, or HIGH.

Maintenance Note:
{note}

Return only:
LOW
MEDIUM
HIGH
""",

    "Role Prompting": """
You are a senior plant safety coordinator responsible for worker safety.

Review the maintenance note and classify its urgency.

Maintenance Note:
{note}

Return only:
LOW
MEDIUM
HIGH
""",

    "Few Shot": """
Classify the urgency.

Example 1

Maintenance Note:
Backup generator tested successfully.
Urgency:
LOW

Example 2

Maintenance Note:
Boiler pressure valve stuck and steam leaking.
Urgency:
HIGH

Maintenance Note:
{note}

Urgency:
""",

    "Chain of Thought": """
Think step by step.

1. Identify the equipment.
2. Determine whether there is a safety risk.
3. Determine whether production is affected.
4. Decide whether immediate action is needed.

Finally classify the urgency as LOW, MEDIUM, or HIGH.

Maintenance Note:
{note}
""",

    "Structured Output": """
Return ONLY valid JSON.

{
    "urgency": "LOW | MEDIUM | HIGH",
    "reason": "One sentence"
}

Maintenance Note:
{note}
"""
}

results = []

for style_name, prompt in styles.items():

    print("=" * 80)
    print(style_name)
    print("=" * 80)

    for note in test_notes:

        try:
            response = client.messages.create(
                model="claude-sonnet-5",
                max_tokens=200,
                messages=[
                    {
                        "role": "user",
                        "content": prompt.format(note=note)
                    }
                ]
            )

            # Extract only text blocks (ignores ThinkingBlock)
            text_blocks = []

            for block in response.content:
                if getattr(block, "type", "") == "text":
                    text_blocks.append(block.text)

            output = "\n".join(text_blocks).strip()

            if not output:
                output = "No text response returned."

            print("NOTE:")
            print(note)
            print()

            print("OUTPUT:")
            print(output)
            print("-" * 80)

            results.append({
                "style": style_name,
                "note": note,
                "output": output
            })

        except Exception as e:
            print(f"Error processing note: {note}")
            print(e)
            print("-" * 80)

# Save results
with open("exercise1_results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)

print("\nAll results saved successfully.")