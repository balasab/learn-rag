# 03 Advanced RAG: Improving Retrieval

This folder explores advanced techniques to fix common RAG failures (e.g., retrieving irrelevant documents that just happen to share keywords).

## Techniques

### 1. Hybrid Search (`hybrid_search.py`)
Combines **Sparse Retrieval** (Keywords/BM25) with **Dense Retrieval** (Embeddings/Vector Search).
- **Why?** Keyword search is great for exact matches (names, model numbers) where vectors fail. Vector search is great for concepts. Combining them gives the best of both.

### 2. Re-ranking (`reranker.py`)
Uses a powerful (but slow) **Cross-Encoder** model to re-score the top documents retrieved by the fast vector DB.
- **Why?** Vector search compresses text into a single vector, losing nuance. A Cross-Encoder looks at the full Query + Document pair to see if they actually match.

### 3. Query Expansion (`query_expansion.py`)
Uses an LLM to generate synonyms or sub-questions from the user's query.
- **Why?** If the user asks "How do I fix the broken thing?", a retriever might fail. Expanding it to "Repairing device X failure modes" helps.

## How to Run

1.  Make sure you ran the Ingestion step in `02_Intermediate_RAG` first!
2.  Install `scikit-learn` (for TF-IDF):
    ```sh
    pip install scikit-learn
    ```
3.  Run the scripts:
    ```sh
    python hybrid_search.py
    python reranker.py
    ```
