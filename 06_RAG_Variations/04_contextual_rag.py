"""
04. Contextual RAG
==================

RAG that uses EXTRA context (User Profile, Location, Time, Device) to filter or bias retrieval.

Flow:
1. User Query + User Context (e.g., Role=Admin, Loc=NY)
2. Vector Search (Filter: Role in [Admin, Public] AND metadata.loc == NY)
3. Filtered Results -> LLM -> Answer

Why do we need this?
- A query like "What are the holiday policies?" has different answers for a Contractor vs. Full-time Employee.
- A query like "Restaurants near me" needs location context.
- Without this, RAG returns generic or incorrect info for the specific user.
"""

class ContextualRAG:
    def __init__(self):
        # Mock database with metadata
        self.db = [
            {"content": "Full-time employees get 20 days PTO.", "role": "full_time", "region": "US"},
            {"content": "Contractors get 0 days PTO.", "role": "contractor", "region": "US"},
            {"content": "European employees get 30 days PTO.", "role": "full_time", "region": "EU"}
        ]

    def retrieve(self, query, user_context):
        print(f"Query: '{query}' | Context: {user_context}")
        
        results = []
        for doc in self.db:
            # 1. Content Relevance (Mock)
            if "policy" in query.lower() or "pto" in query.lower():
                
                # 2. Context Filtering (The Key Part)
                # Check Role Match
                if doc["role"] != user_context["role"]:
                    continue
                
                # Check Region Match
                if doc["region"] != user_context["region"]:
                    continue

                results.append(doc["content"])
        
        return results

    def run(self, query, user_details):
        print("--- Contextual Search ---")
        docs = self.retrieve(query, user_details)
        if docs:
            print(f"Retrieved: {docs}")
            print(f"Answer: {docs[0]}")
        else:
            print("Retrieved: [] (No matching docs for this context)")
        print("")

if __name__ == "__main__":
    rag = ContextualRAG()
    
    # Scene 1: US Contractor asks about PTO
    rag.run("What is my PTO policy?", {"role": "contractor", "region": "US"})
    
    # Scene 2: EU Full-time Employee asks about PTO
    rag.run("What is my PTO policy?", {"role": "full_time", "region": "EU"})
