# Learn RAG: From Basic to Expert

Welcome to the **Retrieval-Augmented Generation (RAG)** Learning Repository!
This repo is designed to take you from knowing nothing about RAG to building Privacy-aware, Agentic RAG systems.

## Curriculum

### [01. Basic RAG](./01_Basic_RAG)
Start here. No external libraries, just pure Python logic to understand the core flow: **Retrieve -> Augment -> Generate**.

### [02. Intermediate RAG](./02_Intermediate_RAG)
Production-ready components.
-   **Vector Database**: ChromaDB
-   **Embeddings**: SentenceTransformers
-   **Chunking**: Breaking text into meaningful pieces.

### [03. Advanced RAG](./03_Advanced_RAG)
When simple vector search fails.
-   **Hybrid Search**: Combining Keywords + Vectors.
-   **Re-ranking**: Fixing ordering with Cross-Encoders.
-   **Query Expansion**: Rewriting user queries for better results.

### [04. Privacy & Redaction](./04_Privacy_and_Redaction)
**[User Requested]** Protecting PII.
-   **Presidio**: Redacting Phones, Emails, Names before they hit the DB.
-   **Safe Retrieval**: Checking docs before sending to LLM.

### [05. Expert RAG](./05_Expert_RAG)
The bleeding edge.
-   **Agentic RAG**: Tools that decide *when* to search.
-   **Evaluation**: Measuring Faithfulness and Relevance (RAGAS concepts).

## Getting Started

1.  **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    python -m spacy download en_core_web_lg
    ```

2.  **Follow the Folders**:
    Go into each folder (starting from 01) and read the `README.md` inside. Run the scripts to see concepts in action.

## License
MIT
