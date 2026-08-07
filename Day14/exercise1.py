"""
Exercise 1 - Build a RAG Pipeline Over an Operations Manual
Run with:  python exercise1.py
"""

from rag_pipeline import chunk_manual, build_collection, ask_claude_grounded, MANUAL

####################################################
# Task 1: Chunk and Embed the Source Document
#####################################################
print("=" * 60)
print("TASK 1: Chunking and storing the manual")
print("=" * 60)

chunks = chunk_manual(MANUAL, chunk_size=300, chunk_overlap=40)
print(f"Created {len(chunks)} chunks.\n")
for i, c in enumerate(chunks, start=1):
    print(f"--- chunk_{i} ---\n{c.strip()}\n")

collection = build_collection(chunks, reset=True)
print("Chunks stored successfully in the 'operations_manual' vector store.\n")

#############################################################
# Task 2: Build the Retrieval Chain + ask the 3 questions
#############################################################
print("=" * 60)
print("TASK 2: Retrieval-augmented answers")
print("=" * 60)

questions = [
    "How often should Pump 4 be inspected?",
    "What is the belt replacement schedule for conveyors?",
    "What is the warranty period for the HVAC system?",  # NOT in the manual
]

for q in questions:
    print(f"\nQ: {q}")
    answer, sections, retrieved = ask_claude_grounded(collection, q, k=3, temperature=0.0)
    print(f"A: {answer}")

####################################################################
# Task 3: Verify Citations
#####################################################################
print("\n" + "=" * 60)
print("TASK 3: Verified citations")
print("=" * 60)

for q in questions:
    print(f"\nQ: {q}")
    answer, sections, retrieved = ask_claude_grounded(collection, q, k=2, temperature=0.0)

    print("Retrieved chunks:")
    for chunk_id, doc, meta in retrieved:
        print(f"  [{chunk_id}] Section {meta['section']}: {doc.strip()[:80]}...")

    print(f"\nFinal Answer:\n{answer}")
    print("\nVerified citations:")
    for s in sections:
        print(f"  ✓ Section {s}")