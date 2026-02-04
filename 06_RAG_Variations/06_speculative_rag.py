"""
06. Speculative RAG
===================

Generating multiple "perspectives" or "sub-questions" to ensure full coverage.

Flow:
1. User Query -> LLM -> Generate 3 Variations/Angles
2. For each Variation -> Vector Search -> Results
3. Aggregate All Results -> LLM -> Final Answer

Why do we need this?
- User queries are often vague: "Tell me about Apple."
- Does he mean the fruit? The company stock? The history? The new iPhone?
- Speculative RAG generates: "Apple fruit nutrition", "Apple Inc stock", "Apple company history".
- Ensures high recall for broad topics.
"""

class SpeculativeRAG:
    def __init__(self):
        pass

    def generate_perspectives(self, query):
        print(f"[Speculator] Brainstorming angles for: '{query}'")
        # Simulation
        if "apple" in query.lower():
            return [
                "Apple (Technology Company) financials",
                "Apple (Fruit) nutritional value",
                "Apple Records (The Beatles label)"
            ]
        return [query]

    def retrieve(self, sub_queries):
        all_docs = []
        for q in sub_queries:
            print(f"   -> Searching for: '{q}'")
            # Mock retrieval
            if "Company" in q:
                all_docs.append("Doc: Apple Inc revenue is $300B.")
            elif "Fruit" in q:
                all_docs.append("Doc: Apples contain fiber.")
        return all_docs

    def run(self, query):
        print(f"--- Processing: '{query}' ---")
        
        # Step 1: Speculate
        perspectives = self.generate_perspectives(query)
        print(f"   (Perspectives: {perspectives})")

        # Step 2: Retrieve for all
        docs = self.retrieve(perspectives)
        
        # Step 3: Synthesize
        print(f"   (Aggregated Context: {docs})")
        print("Final Answer: Covers both the tech giant and the fruit.")
        print("")

if __name__ == "__main__":
    rag = SpeculativeRAG()
    rag.run("Tell me about Apple")
