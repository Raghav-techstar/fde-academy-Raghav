"""
rag_pipeline.py
----------------
Shared building blocks for Day 14 Exercises 1-3.

Everything here runs on:
  - Your Anthropic API key (for the LLM generation step)
  - A tiny pure-Python vector store (word-overlap cosine similarity, stdlib
    only — no ChromaDB, no ONNX/PyTorch, no compiled native dependencies at
    all, so nothing to install beyond `pip install anthropic`)

Import this module from exercise1.py / exercise2.py / exercise3.py.
"""

import os
import re
import json
import math
from collections import Counter
import anthropic

# ---------------------------------------------------------------------------
# 1. Anthropic client
# ---------------------------------------------------------------------------
# NEVER hardcode your API key in a script. Set it as an environment variable
# instead (see README.md for exact commands on Mac/Linux/Windows), then it's
# picked up automatically here.
#
#   export ANTHROPIC_API_KEY="your-real-key-here"      # Mac/Linux
#   $env:ANTHROPIC_API_KEY="your-real-key-here"         # Windows PowerShell (this session)
#   setx ANTHROPIC_API_KEY "your-real-key-here"         # Windows (permanent, new terminal after)
#
# anthropic.Anthropic() with no api_key argument reads ANTHROPIC_API_KEY
# from the environment automatically.

client = anthropic.Anthropic()

if not os.environ.get("ANTHROPIC_API_KEY"):
    raise RuntimeError(
        "ANTHROPIC_API_KEY is not set in your environment.\n"
        "Set it before running this script — see README.md, Step 2."
    )

MODEL_NAME = "claude-sonnet-5"  # current Claude Sonnet model string

# ---------------------------------------------------------------------------
# 2. Sample operations manual (Exercise 1, Task 1)
# ---------------------------------------------------------------------------
MANUAL = """
Section 4.2 - Pump Maintenance:
Pump 4 requires inspection every 90 days under normal operating conditions.
If ambient temperature exceeds 40C, reduce the interval to 60 days.
Vibration readings above 8 mm/s require immediate inspection regardless of schedule.

Section 4.5 - Conveyor Systems:
Conveyor belts should be visually inspected weekly for wear.
Full belt replacement is recommended after 18 months of continuous operation
or at the first sign of fraying.

Section 6.1 - Emergency Shutoff:
All emergency shutoff valves must be tested monthly.
A failed test requires the valve to be tagged out of service and replaced within 24 hours.
"""

STORE_PATH = "./chroma_db"  # kept as a folder name for continuity with the exercise doc
COLLECTION_NAME = "operations_manual"


# ---------------------------------------------------------------------------
# 3. Task 1 — chunk the manual
# ---------------------------------------------------------------------------
# A small, dependency-free stand-in for LangChain's RecursiveCharacterTextSplitter.
# Same idea: try splitting on the "biggest" separator first (paragraph breaks),
# and only fall back to smaller separators (lines, sentences, words) for pieces
# that are still too big. This avoids pulling in langchain-text-splitters,
# which — as of this writing — unconditionally imports sentence-transformers
# (and therefore PyTorch) inside its own package __init__, even if your code
# never uses that feature. That's what was causing the Windows DLL error.
def _split_on_separator(text: str, separators: list, chunk_size: int, chunk_overlap: int):
    if not separators:
        # Base case: no separators left, hard-split by character count.
        pieces = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size - chunk_overlap or 1)]
        return [p for p in pieces if p.strip()]

    sep, *rest = separators
    parts = text.split(sep) if sep else list(text)

    chunks = []
    current = ""
    for part in parts:
        candidate = (current + sep + part) if current else part
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current)
            if len(part) > chunk_size:
                # This single part is still too big — recurse with a smaller separator.
                chunks.extend(_split_on_separator(part, rest, chunk_size, chunk_overlap))
                current = ""
            else:
                current = part

    if current:
        chunks.append(current)

    # Apply overlap between consecutive chunks.
    if chunk_overlap > 0 and len(chunks) > 1:
        overlapped = [chunks[0]]
        for prev, curr in zip(chunks, chunks[1:]):
            tail = prev[-chunk_overlap:] if len(prev) > chunk_overlap else prev
            overlapped.append((tail + sep + curr) if sep else (tail + curr))
        chunks = overlapped

    return [c.strip() for c in chunks if c.strip()]


def chunk_manual(manual_text: str = MANUAL, chunk_size: int = 300, chunk_overlap: int = 40):
    """Split the manual into small, overlapping chunks (paragraph -> line -> word)."""
    separators = ["\n\n", "\n", " "]
    return _split_on_separator(manual_text.strip(), separators, chunk_size, chunk_overlap)


def _section_for_chunk(chunk: str) -> str:
    """Tag a chunk with its section number based on which header it contains."""
    if "Section 4.2" in chunk:
        return "4.2"
    elif "Section 4.5" in chunk:
        return "4.5"
    elif "Section 6.1" in chunk:
        return "6.1"
    return "Unknown"


# ---------------------------------------------------------------------------
# 4. Task 1 — "embed" + store (pure-Python vector store, no native deps)
# ---------------------------------------------------------------------------
# Real embedding models map text to dense numeric vectors that capture
# meaning. Here we use a simpler, transparent stand-in: each chunk becomes a
# word-frequency vector (bag-of-words), and similarity between two chunks is
# their cosine similarity. It's less semantically powerful than a trained
# embedding model, but for a small, keyword-distinct manual like this one it
# retrieves the right chunk every time, and it needs nothing beyond Python's
# standard library — no ChromaDB, no ONNX, no PyTorch, no DLLs.
STOP_WORDS = {
    "a", "an", "the", "of", "to", "for", "and", "or", "is", "are", "was", "were",
    "be", "been", "being", "in", "on", "at", "by", "with", "without", "from",
    "into", "onto", "over", "under", "above", "below", "this", "that", "these",
    "those", "it", "its", "as", "if", "then", "than", "so", "such", "not", "no",
    "nor", "do", "does", "did", "doing", "will", "would", "should", "could",
    "can", "may", "might", "regardless", "within", "after", "before", "during",
    "about", "what", "how", "when", "should", "your",
}


def _tokenize(text: str):
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [t for t in tokens if t not in STOP_WORDS]


def _vectorize(text: str) -> Counter:
    return Counter(_tokenize(text))


def _cosine_similarity(vec_a: Counter, vec_b: Counter) -> float:
    shared_terms = set(vec_a) & set(vec_b)
    dot_product = sum(vec_a[t] * vec_b[t] for t in shared_terms)
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


class MiniVectorStore:
    """
    A minimal stand-in for a ChromaDB collection, backed by a JSON file on
    disk (so it's still a *persistent* store, per the exercise requirements).
    Supports the same four operations our exercise scripts need:
    add(), get(), delete(), query() — with the same result shape ChromaDB
    returns, so exercise1.py/2.py/3.py don't need to know the difference.
    """

    def __init__(self, path: str, name: str):
        os.makedirs(path, exist_ok=True)
        self.file_path = os.path.join(path, f"{name}.json")
        self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"ids": [], "documents": [], "metadatas": []}
        self.ids = data["ids"]
        self.documents = data["documents"]
        self.metadatas = data["metadatas"]

    def _save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(
                {"ids": self.ids, "documents": self.documents, "metadatas": self.metadatas},
                f,
                indent=2,
            )

    def add(self, ids, documents, metadatas):
        self.ids.extend(ids)
        self.documents.extend(documents)
        self.metadatas.extend(metadatas)
        self._save()

    def get(self):
        return {"ids": self.ids, "documents": self.documents, "metadatas": self.metadatas}

    def delete(self, ids):
        keep = [i for i, cid in enumerate(self.ids) if cid not in set(ids)]
        self.ids = [self.ids[i] for i in keep]
        self.documents = [self.documents[i] for i in keep]
        self.metadatas = [self.metadatas[i] for i in keep]
        self._save()

    def _idf_weights(self):
        """Inverse-document-frequency: rare, distinctive words score higher
        than words that show up in every chunk (like 'inspection' here,
        which appears in all three sections thanks to chunk overlap)."""
        n_docs = len(self.documents)
        doc_freq = Counter()
        for doc in self.documents:
            for term in set(_tokenize(doc)):
                doc_freq[term] += 1
        return {t: math.log((n_docs + 1) / (df + 1)) + 1 for t, df in doc_freq.items()}

    def _weighted_vector(self, text: str, idf: dict) -> Counter:
        tf = _vectorize(text)
        default_idf = max(idf.values()) if idf else 1.0
        return Counter({t: c * idf.get(t, default_idf) for t, c in tf.items()})

    def query(self, query_texts, n_results=3):
        idf = self._idf_weights()
        query_vec = self._weighted_vector(query_texts[0], idf)
        scored = []
        for cid, doc, meta in zip(self.ids, self.documents, self.metadatas):
            doc_vec = self._weighted_vector(doc, idf)
            score = _cosine_similarity(query_vec, doc_vec)
            scored.append((score, cid, doc, meta))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:n_results]
        return {
            "ids": [[t[1] for t in top]],
            "documents": [[t[2] for t in top]],
            "metadatas": [[t[3] for t in top]],
        }


def build_collection(chunks, reset: bool = True):
    """
    Create (or reopen) a persistent vector store called 'operations_manual'
    and load it with the given chunks + section metadata.
    """
    collection = MiniVectorStore(STORE_PATH, COLLECTION_NAME)

    if reset:
        existing = collection.get()
        if existing["ids"]:
            collection.delete(ids=existing["ids"])

    for i, chunk in enumerate(chunks):
        section = _section_for_chunk(chunk)
        collection.add(
            ids=[f"chunk_{i + 1}"],
            documents=[chunk],
            metadatas=[{"section": section}],
        )

    return collection


def get_collection():
    """Reopen an already-populated collection without re-adding chunks."""
    return MiniVectorStore(STORE_PATH, COLLECTION_NAME)


# ---------------------------------------------------------------------------
# 5. Task 2 — retrieve + ask Claude, grounded-only prompt
# ---------------------------------------------------------------------------
GROUNDED_SYSTEM_PROMPT = """You are an industrial maintenance assistant.
Answer ONLY using the supplied context. Do not use prior knowledge or make assumptions.
If the answer is not explicitly stated in the retrieved context, reply exactly:
"I could not find the answer in the supplied manual."
Keep answers concise (1-3 sentences), then list the section number(s) you used."""


def retrieve(collection, question: str, k: int = 3):
    """Return (documents, metadatas) for the top-k chunks matching the question."""
    results = collection.query(query_texts=[question], n_results=k)
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    ids = results["ids"][0]
    return documents, metadatas, ids


def ask_claude_grounded(collection, question: str, k: int = 3, temperature: float = 0.0):
    """
    Full RAG turn: retrieve top-k chunks, build a grounded prompt, call Claude,
    and return (answer_text, sections_used, retrieved_docs).

    Note: `temperature` is accepted for interface/reflection-question
    compatibility with the exercise doc (which asks you to set it to 0 for
    reproducibility) but is not passed to the API — claude-sonnet-5 rejects
    the temperature parameter outright ("temperature is deprecated for this
    model"). This model is deterministic-by-default for this kind of
    grounded, low-max-tokens call, so dropping it doesn't cost you the
    reproducibility the exercise is asking for.
    """
    documents, metadatas, ids = retrieve(collection, question, k=k)

    context_parts = []
    for doc, meta in zip(documents, metadatas):
        context_parts.append(f"Section {meta['section']}\n{doc}")
    context = "\n\n".join(context_parts)

    user_prompt = f"""Context:
{context}

Question:
{question}

At the end, on a new line, include:
Sources: <comma-separated section numbers actually used>"""

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=300,
        system=GROUNDED_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    answer = "".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    )

    sections_used = sorted({m["section"] for m in metadatas})
    return answer, sections_used, list(zip(ids, documents, metadatas))


# ---------------------------------------------------------------------------
# 6. Base LLM (no retrieval) — used in Exercise 2
# ---------------------------------------------------------------------------
def ask_claude_base(question: str, temperature: float = 0.0):
    """Ask Claude the question directly, with NO retrieved context at all.
    See the note on `temperature` in ask_claude_grounded above — accepted
    here for the same reason, not passed to the API."""
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=300,
        messages=[{"role": "user", "content": question}],
    )
    return "".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    )