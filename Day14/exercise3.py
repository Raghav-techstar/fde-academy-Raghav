"""
Exercise 3 - Evaluate Retrieval Quality with Precision & Recall
Run AFTER exercise1.py has populated the vector store.
Run with:  python exercise3.py
"""

from rag_pipeline import get_collection, chunk_manual, build_collection, MANUAL

collection = get_collection()

##################################
# Task 1: Build a Test Set
##################################
# First, inspect what's actually stored so the "correct" chunk_ids below are
# accurate rather than guessed (this is exactly what the hint tells you to do).
print("=" * 60)
print("Inspecting stored chunks (collection.get())")
print("=" * 60)
stored = collection.get()
for cid, doc, meta in zip(stored["ids"], stored["documents"], stored["metadatas"]):
    print(f"{cid} (section {meta['section']}): {doc.strip()[:90]}...")


def find_chunk_ids_containing(keyword: str):
    """Helper: return the chunk_ids whose text contains `keyword` (case-insensitive)."""
    matches = []
    for cid, doc in zip(stored["ids"], stored["documents"]):
        if keyword.lower() in doc.lower():
            matches.append(cid)
    return set(matches)


# Ground truth built by keyword-matching against the real stored chunks above,
# rather than hand-guessed IDs (which would drift if chunking parameters change).
test_set = [
    {
        "question": "How often should Pump 4 be inspected?",
        "relevant_chunk_ids": find_chunk_ids_containing("90 days"),
    },
    {
        "question": "What triggers an immediate pump inspection regardless of schedule?",
        "relevant_chunk_ids": find_chunk_ids_containing("Vibration"),
    },
    {
        "question": "How often are conveyor belts visually inspected?",
        "relevant_chunk_ids": find_chunk_ids_containing("visually inspected"),
    },
    {
        "question": "What happens if an emergency shutoff valve fails its monthly test?",
        "relevant_chunk_ids": find_chunk_ids_containing("tagged out of service"),
    },
    {
        # 5th question — written against a fact that's in the manual excerpt.
        "question": "What is the maximum vibration reading before a pump needs inspecting?",
        "relevant_chunk_ids": find_chunk_ids_containing("8 mm/s"),
    },
]

print("\n" + "=" * 60)
print("TASK 1: Test set with ground-truth chunk IDs")
print("=" * 60)
for item in test_set:
    print(item)

##############################################
# Task 2: Compute Precision and Recall
##############################################
def evaluate_retrieval(test_set, collection, k=3):
    results = []
    for item in test_set:
        retrieved = collection.query(query_texts=[item["question"]], n_results=k)
        retrieved_ids = set(retrieved["ids"][0])
        relevant_ids = item["relevant_chunk_ids"]

        true_positives = retrieved_ids & relevant_ids
        precision = len(true_positives) / len(retrieved_ids) if retrieved_ids else 0.0
        recall = len(true_positives) / len(relevant_ids) if relevant_ids else 0.0

        results.append({
            "question": item["question"],
            "retrieved_ids": retrieved_ids,
            "relevant_ids": relevant_ids,
            "precision": precision,
            "recall": recall,
        })
    return results


print("\n" + "=" * 60)
print("TASK 2: Precision / Recall @ k=3")
print("=" * 60)

results = evaluate_retrieval(test_set, collection, k=3)
for r in results:
    print(r)

avg_precision = sum(r["precision"] for r in results) / len(results)
avg_recall = sum(r["recall"] for r in results) / len(results)
print(f"\nAverage precision: {avg_precision:.2f}")
print(f"Average recall: {avg_recall:.2f}")

#################################
# Task 3: Diagnose and Tune
#################################
print("\n" + "=" * 60)
print("TASK 3: Diagnose and tune")
print("=" * 60)
print(f"BEFORE TUNING -> avg precision: {avg_precision:.2f}, avg recall: {avg_recall:.2f}")

# Simple diagnosis heuristic — you should read the actual numbers and reason
# about it yourself, this just prints a starting hypothesis:
if avg_precision < avg_recall:
    print("DIAGNOSIS: precision is the weaker metric -> retriever is pulling back")
    print("too many chunks relative to what's relevant (k may be too high, or chunks")
    print("are too small/fragmented so multiple near-duplicates get retrieved).")
    print("CHANGE APPLIED: reducing k from 3 to 2.")
    tuned_results = evaluate_retrieval(test_set, collection, k=2)
elif avg_recall < avg_precision:
    print("DIAGNOSIS: recall is the weaker metric -> the retriever is missing")
    print("relevant chunks entirely (k may be too low, or chunk boundaries are")
    print("splitting a fact away from the section that discusses it).")
    print("CHANGE APPLIED: increasing k from 3 to 5.")
    tuned_results = evaluate_retrieval(test_set, collection, k=5)
else:
    print("DIAGNOSIS: precision and recall are balanced already.")
    print("CHANGE APPLIED (control run): re-running at k=3 with chunk_overlap")
    print("increased from 40 to 80, to test whether more overlap changes anything.")
    chunks = chunk_manual(MANUAL, chunk_size=300, chunk_overlap=80)
    collection = build_collection(chunks, reset=True)
    tuned_results = evaluate_retrieval(test_set, collection, k=3)

avg_precision_after = sum(r["precision"] for r in tuned_results) / len(tuned_results)
avg_recall_after = sum(r["recall"] for r in tuned_results) / len(tuned_results)
print(f"\nAFTER TUNING -> avg precision: {avg_precision_after:.2f}, avg recall: {avg_recall_after:.2f}")