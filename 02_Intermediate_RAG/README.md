# 02 Intermediate RAG: Vector Databases & Embeddings

This folder moves beyond simple keyword matching to **Semantic Search** using Vector Databases.

## Key Concepts

1.  **Embeddings**: Converting text into numerical logic vectors (lists of numbers) that capture meaning.
2.  **Vector Database (ChromaDB)**: A specialized database optimized for storing and querying these vectors fast.
3.  **Semantic Search**: Finding documents that mean the same thing, even if they use different words (e.g., "automobile" approx. "car").

## Files

-   `ingestion.py`: Creates a local ChromaDB, embeds sample text, and stores it.
-   `semantic_search.py`: Connects to the database and performs similarity searches.

## How to Run

1.  Install dependencies:
    ```sh
    pip install -r ../requirements.txt
    ```
2.  Run ingestion (creates the DB in `chroma_db_data/`):
    ```sh
    python ingestion.py
    ```
3.  Run search:
    ```sh
    python semantic_search.py
    ```
