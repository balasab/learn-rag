# 05 Expert RAG: Agents & Evaluation

This final level covers "Agentic" workflows and how to measure if your RAG system is actually working.

## Concepts

### 1. Agentic RAG (`agentic_rag.py`)
Instead of a linear pipeline (Retrieve -> Generate), an **Agent** decides **what** to do.
- It might use a Search Tool, a Calculator, or a SQL DB tool depending on the user request.
- It can "loop" (think -> act -> observe) to gather multi-step info.

### 2. Evaluation (`evaluation.py`)
How do you know `k=5` key chunks is better than `k=3`? Or if Vector Search is better than Keyword?
You need metrics.
- **Faithfulness**: Is the answer actually in the retrieved docs? (Hallucination check).
- **Answer Relevance**: Did we answer the user's question?
- **Context Precision**: Did we retrieve the right document first?
- **Tools**: [Ragas](https://github.com/explodinggradients/ragas), [DeepEval](https://github.com/confident-ai/deepeval).

## How to Run

1.  Run the agent:
    ```sh
    python agentic_rag.py
    ```
2.  Run the eval demo:
    ```sh
    python evaluation.py
    ```
