"""
02. Multi-Stage Pipeline (Reranking)
====================================

Demonstrating the "Retrieve -> Rerank" funnel.

Stage 1: Bi-Encoder (Vector Search)
- Speed: Fast (ms)
- Accuracy: Good
- Output: Top-50 "Maybe" relevant docs

Stage 2: Cross-Encoder (Reranker)
- Speed: Slow (s)
- Accuracy: Excellent
- Output: Top-5 "Definitely" relevant docs
"""

class MultiStageRAG:
    def __init__(self):
        # Mock Corpus
        self.docs = [
            {"id": 1, "text": "Apple is a fruit rich in fiber."},
            {"id": 2, "text": "Apple Inc. produces the iPhone."},
            {"id": 3, "text": "Dr. Apple is a famous surgeon."},
            {"id": 4, "text": "Apples grow on trees."},
            {"id": 5, "text": "Apple stock symbol is AAPL."}
        ]

    def stage_1_vector_search(self, query):
        print(f"[Stage 1] Vector Search for: '{query}'")
        # Creating a "rough" list based on keyword overlap (simulating vector similarity)
        # In reality, this uses cosine similarity
        results = [d for d in self.docs if "Apple" in d["text"]]
        print(f" -> Found {len(results)} initial candidates.")
        return results

    def stage_2_reranker(self, query, initial_docs):
        print(f"[Stage 2] Cross-Encoder Reranking...")
        scored_results = []
        
        for doc in initial_docs:
            score = 0
            # Simulating a Cross-Encoder that understands context better
            if "fruit" in query and "fruit" in doc["text"]:
                score = 0.99
            elif "fruit" in query and "trees" in doc["text"]:
                score = 0.80
            elif "tech" in query and "Inc" in doc["text"]:
                score = 0.99
            elif "tech" in query and "stock" in doc["text"]:
                score = 0.90
            else:
                score = 0.10 # Irrelevant to the specific intent
            
            scored_results.append((doc, score))
            print(f"   -> Doc {doc['id']} Score: {score}")

        # Sort by Score descending
        scored_results.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in scored_results[:2]] # Return Top-2

    def run(self, query):
        print(f"--- Pipeline Start: '{query}' ---")
        
        # 1. Retrieve
        candidates = self.stage_1_vector_search(query)
        
        # 2. Rerank
        final_top_k = self.stage_2_reranker(query, candidates)
        
        print(f"\n[Final Output] Top Recommended Docs:")
        for doc in final_top_k:
            print(f" - {doc['text']}")
        print("\n")

if __name__ == "__main__":
    rag = MultiStageRAG()
    
    # Query 1: Fruit Intent
    rag.run("Tell me about the fruit Apple")
    
    # Query 2: Tech Intent
    rag.run("Tell me about the tech company Apple")
