# 06. RAG Variations

This directory explores advanced architectural patterns and techniques for Retrieval-Augmented Generation (RAG).

## Architectures

### 1. Classic RAG
The standard "Retrieve -> Augment -> Generate" loop.
-   **File**: `01_classic_rag.py`
-   **Use Case**: Simple Q&A, standard document search.

### 2. Branched RAG
Routing queries to different RAG pipelines based on intent.
-   **File**: `02_branched_rag.py`
-   **Use Case**: Handling mixed queries (e.g., "Summarize this PDF" vs. "What is the stock price of Apple?").

### 3. Memory-Enhanced RAG
Adding conversation history to the context.
-   **File**: `03_memory_enhanced_rag.py`
-   **Use Case**: Chatbots, multi-turn conversations.

### 4. Contextual RAG
Injecting global context (e.g., user profile, location) into the retrieval.
-   **File**: `04_contextual_rag.py`
-   **Use Case**: Personalized answers, location-aware services.

## Techniques

### 5. HyDe (Hypothetical Document Embeddings)
Generating a fake "ideal" answer and using *that* to search, rather than the raw question.
-   **File**: `05_hyde_rag.py`
-   **Use Case**: Poorly phrased queries, searching for answers based on semantic similarity to the *answer* rather than the question.

### 6. Speculative RAG
Generating multiple potential perspectives or sub-questions to broaden retrieval.
-   **File**: `06_speculative_rag.py`
-   **Use Case**: Comprehensive research, exploring different angles of a topic.
