"""
01. Classic RAG
===============

The "Vanilla" RAG architecture.

Flow:
1. User Query -> Embedding Model -> Query Vector
2. Query Vector -> Vector Database -> Top-K Relevant Chunks
3. Top-K Chunks + Original Query -> LLM -> Answer

Why do we need this?
- Reduces hallucinations by grounding answers in retrieved data.
- Allows LLMs to access private or up-to-date data not in their training set.
"""

import time

class ClassicRAG:
    def __init__(self):
        # Simulation of components
        print("Initializing Classic RAG components...")
        self.knowledge_base = {
            "chunk_1": "RAG stands for Retrieval-Augmented Generation.",
            "chunk_2": "It combines a retriever and a generator.",
            "chunk_3": "The retriever searches a database for relevant info."
        }

    def retrieve(self, query):
        print(f"Retrieving for query: '{query}'")
        # In a real app, this would be: embedding -> vector search
        # Here, we just return a dummy relevant chunk
        return ["chunk_1", "chunk_2"]

    def generate(self, query, context):
        print(f"Generating answer using context: {context}")
        # In a real app, this calls OpenAI/Gemini/Anthropic
        context_text = " ".join([self.knowledge_base[c] for c in context])
        return f"Based on the context ('{context_text}'), here is the answer to '{query}'."

    def run(self, query):
        print("--- Running Classic RAG ---")
        relevant_chunks = self.retrieve(query)
        answer = self.generate(query, relevant_chunks)
        print(f"Final Answer: {answer}\n")

if __name__ == "__main__":
    rag = ClassicRAG()
    rag.run("What is RAG?")
