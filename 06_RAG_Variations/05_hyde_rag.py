"""
05. HyDe (Hypothetical Document Embeddings)
===========================================

Instead of searching with the QUESTION, we search with a hallucinated ANSWER.

Flow:
1. User Query -> LLM -> "Hypothetical Answer" (can be wrong, but semantically dense)
2. Hypothetical Answer -> Embedding Model -> Vector
3. Vector -> Vector Database -> Real Documents
4. Real Documents + User Query -> LLM -> Final Answer

Why do we need this?
- Vector search relies on semantic similarity.
- "How do I fix error 500?" (Question) is not semantically similar to "Error 500 is caused by..." (Answer).
- But the Hypothetical Answer "To fix error 500, check logs..." IS similar to the real documentation.
- It bridges the "Question-Answer Gap".
"""

class HyDeRAG:
    def __init__(self):
        pass

    def generate_hypothetical_answer(self, query):
        print(f"[HyDe] Generating fake answer for: '{query}'")
        # LLM Hallucination Simulation
        if "policy" in query:
            return "The return policy allows for returns within 30 days if the item is unused."
        return "Generic hypothetical answer about " + query

    def retrieve(self, search_query):
        print(f"[Retrieve] Vector searching with: '{search_query}'")
        # Simulation: In real life, this embedding matches the content better than the raw question
        return ["Real Doc: Returns are accepted within 30 days.", "Real Doc: Items must be in original packaging."]

    def run(self, query):
        print(f"--- Processing: '{query}' ---")
        
        # Step 1: Hallucinate
        hypothetical = self.generate_hypothetical_answer(query)
        print(f"   (Hypothetical: '{hypothetical}')")

        # Step 2: Use the Hallucination to Search
        docs = self.retrieve(hypothetical)
        
        # Step 3: Generate Final Answer
        print(f"   (Retrieved Docs: {docs})")
        print("Final Answer based on Real Docs: ...")
        print("")

if __name__ == "__main__":
    rag = HyDeRAG()
    rag.run("What is the return policy?")
