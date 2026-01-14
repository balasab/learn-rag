# 04 Privacy & Redaction in RAG

This folder demonstrates how to handle **Personally Identifiable Information (PII)** in RAG systems.
This is critical for enterprise applications where private user data must not be leaked to the LLM (which might log it) or to other users.

## Tools Used
-   **Microsoft Presidio**: A library for PII detection and redaction.
-   **Spacy**: NLP engine used by Presidio.

## Files

-   `redaction_pipeline.py`: Shows how to detect and replace names, emails, and phone numbers *before* ingestion.
-   `safe_retrieval.py`: Shows how to scan retrieved documents for PII *after* retrieval (as a safety net) before sending to the LLM.

## How to Run

1.  Install dependencies:
    ```sh
    pip install presidio-analyzer presidio-anonymizer spacy
    python -m spacy download en_core_web_lg
    ```
    (Note: `en_core_web_lg` is massive. You can try `en_core_web_sm` if space is tight, but `lg` gives better accuracy).

2.  Run the examples:
    ```sh
    python redaction_pipeline.py
    python safe_retrieval.py
    ```
