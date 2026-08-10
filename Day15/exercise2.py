from typing import TypedDict

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from exercise1 import model, classify_node, extract_node, summarize_node, route_after_classify

TEST_COMPLAINTS = [
    "Account #48213 - My internet has been down for 6 hours and I work "
    "from home. This is costing me money. Fix this NOW.",
    "Ticket #9042 - Billing seems slightly higher this month than usual, "
    "could someone check when convenient? No rush.",
    "Account #77410 - Complete outage across my whole building, multiple "
    "neighbors affected, please escalate immediately.",
    "Just wanted to say the new app update looks nice. Ticket #201.",
]


################################################
# Task 1: Add the Work Order Proposal Node
################################################
class ComplaintState(TypedDict):
    complaint: str
    classification: str
    account_id: str
    summary: str
    proposed_work_order: str  # NEW FIELD
    status: str                # NEW FIELD


work_order_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You draft work orders for field technicians at a telecom operator. "
     "Given a customer complaint and its account ID, write a brief work "
     "order in 2-3 sentences covering: what needs to happen, for which "
     "account, and at what priority (e.g. Priority: High/Critical). "
     "Respond with ONLY the work order text, nothing else."),
    ("human", "Complaint: {complaint}\nAccount ID: {account_id}"),
])

propose_work_order_chain = work_order_prompt | model | StrOutputParser()


def propose_work_order_node(state: ComplaintState) -> dict:
    """Draft a work order for an urgent, already-extracted complaint and
    mark it pending approval — this node runs, then the graph is
    interrupted BEFORE the following dispatch node executes."""
    work_order = propose_work_order_chain.invoke({
        "complaint": state["complaint"],
        "account_id": state["account_id"],
    }).strip()
    return {"proposed_work_order": work_order, "status": "pending_approval"}


def dispatch_node(state: ComplaintState) -> dict:
    """Only reached after a human resumes the graph post-approval."""
    return {"status": "dispatched"}


##################################
# Task 2: Wire the Interrupt
##################################
graph = StateGraph(ComplaintState)

graph.add_node("classify", classify_node)
graph.add_node("extract", extract_node)
graph.add_node("summarize", summarize_node)
graph.add_node("propose_work_order", propose_work_order_node)
graph.add_node("dispatch", dispatch_node)

graph.set_entry_point("classify")
graph.add_conditional_edges(
    "classify",
    route_after_classify,
    {"extract": "extract", "summarize": "summarize"},
)
graph.add_edge("extract", "propose_work_order")
graph.add_edge("propose_work_order", "dispatch")
graph.add_edge("dispatch", END)
graph.add_edge("summarize", END)

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer, interrupt_before=["dispatch"])


##########################################
# Task 3: Simulate Approval and Resume
##########################################
if __name__ == "__main__":
    # Use complaint 1 — urgent, so it will take the extract -> propose_work_order path.
    urgent_complaint = TEST_COMPLAINTS[0]
    config = {"configurable": {"thread_id": "complaint-001"}}

    initial_state: ComplaintState = {
        "complaint": urgent_complaint,
        "classification": "",
        "account_id": "",
        "summary": "",
        "proposed_work_order": "",
        "status": "",
    }

    print("=" * 60)
    print("First invoke() — should stop BEFORE dispatch")
    print("=" * 60)
    result = app.invoke(initial_state, config=config)
    print(f"status: {result['status']}")
    print(f"proposed_work_order: {result['proposed_work_order']}")
    assert result["status"] == "pending_approval", "Graph did not stop at the interrupt as expected."

    # Simulate: print the proposed work order for "human review"
    current_state = app.get_state(config)
    print("\nPENDING APPROVAL:", current_state.values["proposed_work_order"])

    # Simulate approval by resuming the graph — invoke with None as input
    # and the same config. This tells LangGraph to continue from the
    # checkpoint rather than starting a new run.
    input("\nPress Enter to simulate supervisor approval and resume...")

    print("\n" + "=" * 60)
    print("Resuming after approval")
    print("=" * 60)
    final_result = app.invoke(None, config=config)

    print(f"status: {final_result['status']}")
    print(f"proposed_work_order: {final_result['proposed_work_order']}")
    assert final_result["status"] == "dispatched", "Graph did not reach dispatch after resuming."
    print("\nConfirmed: status == 'dispatched'")