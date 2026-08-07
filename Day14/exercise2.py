"""
Exercise 2 - Compare RAG Responses vs. Base LLM
Run AFTER exercise1.py has populated the vector store.
Run with:  python exercise2.py
"""

from rag_pipeline import get_collection, ask_claude_base, ask_claude_grounded

questions = [
    "How often should Pump 4 be inspected?",
    "What is the belt replacement schedule for conveyors?",
    "What is the warranty period for the HVAC system?",  # NOT in the manual
]

##############################################
# Task 1: Run the Base LLM (No Retrieval)
###############################################
print("=" * 60)
print("TASK 1: Base LLM answers (no retrieval, no manual)")
print("=" * 60)

base_answers = []
for q in questions:
    answer = ask_claude_base(q, temperature=0.0)
    base_answers.append(answer)
    print(f"\nQ: {q}\nA: {answer}")

##########################################
# Task 2: Build the Comparison Table
##########################################
print("\n" + "=" * 60)
print("TASK 2: RAG pipeline answers (for the comparison table)")
print("=" * 60)

collection = get_collection()
rag_answers = []
for q in questions:
    answer, sections, _ = ask_claude_grounded(collection, q, k=3, temperature=0.0)
    rag_answers.append(answer)
    print(f"\nQ: {q}\nA: {answer}")

print("\n" + "=" * 60)
print("COMPARISON TABLE (copy these into your portfolio doc)")
print("=" * 60)
labels = ["Pump 4 inspection interval", "Conveyor belt replacement schedule", "HVAC warranty period"]
for label, q, base, rag in zip(labels, questions, base_answers, rag_answers):
    print(f"\n### {label}")
    print(f"Question: {q}")
    print(f"Base LLM Answer: {base}")
    print(f"RAG Pipeline Answer: {rag}")

###############################################
# Task 3: Classify Each Base LLM Answer
################################################
# This step is a judgment call, not something a script should decide for you —
# read each base_answers[i] above and classify it yourself as one of:
#   CORRECT_BY_COINCIDENCE / PLAUSIBLE_BUT_WRONG / APPROPRIATELY_UNCERTAIN
# Fill in the template below once you've read the actual outputs.
print("\n" + "=" * 60)
print("TASK 3: Classification template (fill in after reading Task 1 output)")
print("=" * 60)

for i, q in enumerate(questions, start=1):
    print(f"\nQuestion {i}: {q}")
    print("  Classification: <CORRECT_BY_COINCIDENCE | PLAUSIBLE_BUT_WRONG | APPROPRIATELY_UNCERTAIN>")
    print("  Justification: <why — does it match the manual? confident but wrong? admits uncertainty?>")