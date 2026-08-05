import os
import json
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic

load_dotenv()

llm = ChatAnthropic(
    model="claude-sonnet-5",
    api_key=os.getenv("API KEY"),  # Change to ANTHROPIC_API_KEY if needed
)

executive_summary_generator = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an operations analyst preparing a brief for a time-constrained executive.

Write exactly three sentences:

1. Overall operational performance.
2. Biggest operational risk.
3. Recommended next action.

No jargon.
No bullet points.
""",
        ),
        (
            "user",
            """Dashboard data:

{dashboard_metrics}
""",
        ),
    ]
)

work_order_priority_classifier = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a maintenance operations engineer.

Classify the work order priority.

Possible priorities:

LOW
MEDIUM
HIGH
CRITICAL

Return ONLY JSON.

{{
    "priority":"LOW | MEDIUM | HIGH | CRITICAL",
    "reason":"One sentence",
    "recommended_action":"One sentence"
}}
""",
        ),
        (
            "user",
            """Work Order:

{work_order_text}
""",
        ),
    ]
)

shipment_delay_risk_analyzer = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a supply chain logistics analyst.

Determine the shipment delay risk.

Possible values:

LOW
MEDIUM
HIGH

Return ONLY JSON.

{{
    "risk_level":"LOW | MEDIUM | HIGH",
    "reason":"One sentence",
    "recommended_action":"One sentence"
}}
""",
        ),
        (
            "user",
            """Shipment Details:

{shipment_details}
""",
        ),
    ]
)

TEMPLATES = {
    "executive_summary_generator": executive_summary_generator,
    "work_order_priority_classifier": work_order_priority_classifier,
    "shipment_delay_risk_analyzer": shipment_delay_risk_analyzer,
}

TEST_CASES = {

    "executive_summary_generator": [

        {
            "dashboard_metrics":
            (
                "On-time shipment rate: 91%. "
                "Average delivery delay: 1.8 days. "
                "Warehouse utilization: 88%. "
                "Damaged goods rate: 2.1%. "
                "Fleet fuel cost: $142,000."
            )
        },

        {
            "dashboard_metrics":
            (
                "Order fulfillment: 98%. "
                "Inventory accuracy: 97%. "
                "Late deliveries: 2%. "
                "Customer satisfaction: 95%."
            )
        },

    ],

    "work_order_priority_classifier": [

        {
            "work_order_text":
            "Forklift hydraulic leak, minor, no production impact."
        },

        {
            "work_order_text":
            "Emergency stop button on Line 3 is unresponsive during safety inspection."
        },

    ],

    "shipment_delay_risk_analyzer": [

        {
            "shipment_details":
            "Shipment SH001 delayed by 3 days because of severe weather."
        },

        {
            "shipment_details":
            "Shipment SH002 delivered on time without any issues."
        },

    ],

}

results = {}

for template_name, template in TEMPLATES.items():

    print("=" * 70)
    print(template_name)
    print("=" * 70)

    results[template_name] = []

    for test in TEST_CASES[template_name]:

        prompt = template.invoke(test)

        response = llm.invoke(prompt)

        print("Input:")
        print(test)

        print()

        print("Output:")
        print(response.content)

        print("-" * 70)

        results[template_name].append(
            {
                "input": test,
                "output": response.content,
            }
        )


with open(
    "prompt_template_results.json",
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        results,
        f,
        indent=4,
        ensure_ascii=False,
    )

print("\nResults saved to prompt_template_results.json")