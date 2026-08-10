import re
import time

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from exercise1 import model, extract_chain

##################################################
# Task 1: Create Deliberately Messy Test Inputs
##################################################
messy_complaints = [
    "my service acct is acting up again this is like the third time",
    "Ref: TCK-9042-B / urgent pls advise re: outage",
    "hey so my bill this month??? account thingy is 55231 i think, not sure format",
    "nothing works, please help asap",  # no ID at all
]


def original_extract(complaint: str) -> str:
    """The ORIGINAL Exercise 1 extract_chain, called directly with no
    retry or validation — used as the 'before' baseline."""
    return extract_chain.invoke({"complaint": complaint}).strip()


#####################################################
# Task 2: Build the Retry Wrapper with Validation
#####################################################
def is_valid_id(extracted_text: str) -> bool:
    """True only if extracted_text looks like a real ID: short, and
    containing at least 3 consecutive digits with only ID-like characters
    around them (letters, digits, #, /, -, :, spaces). Rejects empty
    responses, 'NOT_FOUND', and hallucinated full-sentence explanations."""
    if not extracted_text:
        return False
    text = extracted_text.strip()
    if len(text) > 40:
        # A real ID is short. A long response is almost always the model
        # explaining itself or hallucinating a sentence, not returning an ID.
        return False
    if not re.fullmatch(r"[A-Za-z0-9#/\-:. ]+", text):
        return False
    if not re.search(r"\d{3,}", text):
        return False
    return True


def extract_with_retry(complaint: str, max_attempts: int = 3):
    """Call extract_chain up to max_attempts times, validating each
    response. Returns the first valid-looking ID, or None if every
    attempt fails validation (signals 'no valid extraction' — does NOT
    invent a fallback ID)."""
    for attempt in range(1, max_attempts + 1):
        result = extract_chain.invoke({"complaint": complaint}).strip()

        if is_valid_id(result):
            return result

        print(f"  [attempt {attempt}] invalid response: {result!r} — retrying...")
        if attempt < max_attempts:
            backoff_seconds = 2 ** attempt
            time.sleep(min(backoff_seconds, 0.5))  # capped short for a fast demo run

    return None


# ---------------------------------------------------------------------------
# Task 3: Add the Fallback Prompt
# ---------------------------------------------------------------------------
fallback_extract_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Extract an ID from this customer complaint. Look specifically for "
     "any of these patterns: a '#' followed by alphanumeric characters, "
     "'Ref:' followed by alphanumeric characters, 'Ticket' followed by "
     "alphanumeric characters, or 'Account' followed by alphanumeric "
     "characters. Return EXACTLY the matched pattern and nothing else — "
     "no explanation, no punctuation beyond what's in the match. If none "
     "of these patterns appear anywhere in the text, respond with exactly: "
     "NOT_FOUND"),
    ("human", "{complaint}"),
])

fallback_extract_chain = fallback_extract_prompt | model | StrOutputParser()


def extract_with_retry_and_fallback(complaint: str, max_attempts: int = 3) -> str:
    result = extract_with_retry(complaint, max_attempts=max_attempts)
    if result is not None:
        return result

    fallback_result = fallback_extract_chain.invoke({"complaint": complaint}).strip()
    if is_valid_id(fallback_result):
        return fallback_result
    return "NOT_FOUND"


# ---------------------------------------------------------------------------
# Before / after comparison
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("BEFORE (Task 1, original chain):")
    before_results = []
    for complaint in messy_complaints:
        result = original_extract(complaint)
        before_results.append(result)
        print(f"  {complaint!r}\n    -> {result!r}\n")

    print("\nAFTER (retry + fallback):")
    after_results = []
    for complaint in messy_complaints:
        print(f"Extracting: {complaint!r}")
        result = extract_with_retry_and_fallback(complaint)
        after_results.append(result)
        print(f"  -> FINAL: {result!r}\n")

    print("=" * 60)
    print("COMPARISON")
    print("=" * 60)
    for complaint, before, after in zip(messy_complaints, before_results, after_results):
        looks_bad_before = not is_valid_id(before)
        flag = "IMPROVED" if looks_bad_before and (after != "NOT_FOUND" or before != after) else "same"
        print(f"\nComplaint: {complaint!r}")
        print(f"  BEFORE: {before!r}  {'(invalid/hallucinated)' if looks_bad_before else '(looked valid)'}")
        print(f"  AFTER:  {after!r}")