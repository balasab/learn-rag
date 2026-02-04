# 07. Optimization & Tuning

This module covers advanced techniques to improve RAG performance through **Fine-Tuning** and **Multi-Stage Processing**.

## 1. RAFT (Retrieval-Augmented Fine-Tuning)
**File**: [`01_raft.py`](./01_raft.py)

Standard RAG keeps the LLM frozen and only changes the context. **RAFT** fine-tunes the LLM itself to be better at *using* that context.

### The Problem
- LLMs can ignore retrieved context or be distracted by irrelevant chunks ("Lost in the Middle").
- We want the model to learn: "When given context, trust it. When context is missing, admit ignorance."

### The Solution (RAFT)
We train the model on a mix of data:
1.  **Question + Meaningful Documents -> Answer** (Teaches reasoning over docs)
2.  **Question + Distractor Documents -> Answer** (Teaches robustness to noise)

## 2. Multi-Stage Pipeline (Reranking)
**File**: [`02_multistage_pipeline.py`](./02_multistage_pipeline.py)

A "Funnel" approach to retrieval.

### The Problem
- Vector search (Bi-Encoder) is fast but approximate. It often retrieves "sort of relevant" chunks in the top 10.
- Cross-Encoders are very accurate but slow.

### The Solution
1.  **Stage 1 (Retrieve)**: Use fast Vector Search to get Top-50 candidates.
2.  **Stage 2 (Rerank)**: Use a slow, precise Cross-Encoder to re-score those 50 and pick the Top-5.
