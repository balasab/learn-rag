"""
02. Branched RAG (Router)
=========================

A system that decides WHICH pathway to take based on the user's intent.

Flow:
1. User Query -> Semantic Router (Classifier or LLM) -> Intent
2. If Intent == "Technical" -> Search Tech Documentation -> LLM
3. If Intent == "General"   -> Search General Knowledge -> LLM
4. If Intent == "Summarize" -> Skip Search -> Summarize Tool

Why do we need this?
- "One size fits all" RAG performs poorly when queries vary wildly (e.g., asking for code vs. asking for legal advice).
- Optimizes cost and latency by using specialized pipelines.
"""

class BranchedRAG:
    def __init__(self):
        pass

    def router(self, query):
        # Simple keyword-based routing for demonstration
        if "define" in query.lower() or "what is" in query.lower():
            return "definition_pipeline"
        elif "summarize" in query.lower():
            return "summarization_pipeline"
        else:
            return "general_pipeline"

    def definition_pipeline(self, query):
        print("[Router] Selected: Definition Pipeline")
        print("-> Looking up dictionary/glossary...")
        return "Here is the precise definition..."

    def summarization_pipeline(self, query):
        print("[Router] Selected: Summarization Pipeline")
        print("-> Loading full document text...")
        print("-> Generating summary...")
        return "Here is the summary..."

    def general_pipeline(self, query):
        print("[Router] Selected: General Pipeline")
        print("-> Performing standard Vector Search...")
        return "Here is a general answer..."

    def run(self, query):
        print(f"--- Processing: '{query}' ---")
        intent = self.router(query)
        
        if intent == "definition_pipeline":
            response = self.definition_pipeline(query)
        elif intent == "summarization_pipeline":
            response = self.summarization_pipeline(query)
        else:
            response = self.general_pipeline(query)
        
        print(f"Result: {response}\n")

if __name__ == "__main__":
    rag = BranchedRAG()
    rag.run("What is Retrieval-Augmented Generation?")
    rag.run("Summarize the meeting notes.")
    rag.run("How's the weather?")
