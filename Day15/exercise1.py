import os
from typing import TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

if not os.environ.get("ANTHROPIC_API_KEY"):
    raise RuntimeError(
        "ANTHROPIC_API_KEY is not set in your environment.\n"
        "PowerShell: $env:ANTHROPIC_API_KEY=\"API-KEY-HERE\"\n"
    )


model = ChatAnthropic(model="claude-sonnet-5")

TEST_COMPLAINTS = [
    "Account #48213 - My internet has been down for 6 hours and I work "
    "from home. This is costing me money. Fix this NOW.",
    "Ticket #9042 - Billing seems slightly higher this month than usual, "
    "could someone check when convenient? No rush.",
    "Account #77410 - Complete outage across my whole building, multiple "
    "neighbors affected, please escalate immediately.",
    "Just wanted to say the new app update looks nice. Ticket #201.",
]

############################################
# Task 1: Build the 3 independent chains
#############################################
classify_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You triage telecom customer complaints. Read the complaint and decide "
     "if it is URGENT or ROUTINE.\n"
     "URGENT: service outages, complete loss of service, complaints "
     "demanding immediate action, anything costing the customer money right "
     "now, or explicit escalation requests.\n"
     "ROUTINE: billing questions, non-urgent requests, feedback, or "
     "anything the customer says is not time-sensitive.\n"
     "Respond with exactly one word: URGENT or ROUTINE. No punctuation, no "
     "explanation."),
    ("human", "{complaint}"),
])

extract_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Extract the account or ticket ID from this complaint. IDs appear as "
     "'Account #NNNNN' or 'Ticket #NNNNN'. Respond with ONLY the ID exactly "
     "as written (e.g. 'Account #48213' or 'Ticket #9042'), nothing else."),
    ("human", "{complaint}"),
])

summarize_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Summarize this customer complaint in exactly one sentence, for an "
     "internal ticket queue. Be concise and neutral. Respond with ONLY the "
     "summary sentence, nothing else."),
    ("human", "{complaint}"),
])

classify_chain = classify_prompt | model | StrOutputParser()
extract_chain = extract_prompt | model | StrOutputParser()
summarize_chain = summarize_prompt | model | StrOutputParser()


##############################################
# Task 2: Compose the LangGraph workflow
###############################################
class ComplaintState(TypedDict):
    complaint: str
    classification: str
    account_id: str
    summary: str


def classify_node(state: ComplaintState) -> dict:
    classification = classify_chain.invoke({"complaint": state["complaint"]}).strip()
    return {"classification": classification}


def extract_node(state: ComplaintState) -> dict:
    account_id = extract_chain.invoke({"complaint": state["complaint"]}).strip()
    return {"account_id": account_id}


def summarize_node(state: ComplaintState) -> dict:
    summary = summarize_chain.invoke({"complaint": state["complaint"]}).strip()
    return {"summary": summary}


def route_after_classify(state: ComplaintState) -> str:
    return "extract" if "URGENT" in state["classification"].upper() else "summarize"


graph = StateGraph(ComplaintState)
graph.add_node("classify", classify_node)
graph.add_node("extract", extract_node)
graph.add_node("summarize", summarize_node)

graph.set_entry_point("classify")
graph.add_conditional_edges(
    "classify",
    route_after_classify,
    {"extract": "extract", "summarize": "summarize"},
)
graph.add_edge("extract", END)
graph.add_edge("summarize", END)

app = graph.compile()


###############################################
# Task 3: Run and trace all 4 complaints
###############################################
if __name__ == "__main__":
    for i, complaint in enumerate(TEST_COMPLAINTS, start=1):
        print("=" * 60)
        print(f"Complaint {i}: {complaint}")
        print("=" * 60)

        initial_state: ComplaintState = {
            "complaint": complaint,
            "classification": "",
            "account_id": "",
            "summary": "",
        }
        final_state = app.invoke(initial_state)

        print(f"classification: {final_state['classification']}")
        print(f"account_id:     {final_state['account_id'] or '(empty)'}")
        print(f"summary:        {final_state['summary'] or '(empty)'}")
        print()