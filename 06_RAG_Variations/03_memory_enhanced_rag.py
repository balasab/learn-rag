"""
03. Memory-Enhanced RAG
=======================

RAG that remembers previous turns in the conversation.

Flow:
1. User Query + Conversation History -> LLM (Reformulation) -> Standalone Query
2. Standalone Query -> Vector Search -> Context
3. Context + History + Query -> LLM -> Answer

Why do we need this?
- Standard RAG treats every query as an isolated event.
- If a user asks "Who is the CEO of Google?" then "How old is he?", standard RAG fails on the second question because "he" is ambiguous without history.
- Memory-Enhanced RAG rewrites the second query to "How old is the CEO of Google?" before searching.
"""

class MemoryEnhancedRAG:
    def __init__(self):
        self.history = []
        self.knowledge = {
            "sundar": "Sundar Pichai is the CEO of Google and Alphabet.",
            "age": "Sundar Pichai was born in 1972 (approx 52 years old)."
        }

    def reformulate_query(self, query):
        if not self.history:
            return query
        
        print(f"   [Memory] History found: {self.history}")
        print("   [Memory] Rewriting query to be standalone...")
        # Simulation of LLM rewriting "How old is he?" -> "How old is Sundar Pichai?"
        if "he" in query.lower() and "sundar" in str(self.history[-1]).lower():
            return "How old is Sundar Pichai?"
        return query

    def retrieve(self, query):
        print(f"   [Retrieve] Searching for: '{query}'")
        if "ceo" in query.lower():
            return self.knowledge["sundar"]
        elif "old" in query.lower() and "sundar" in query.lower():
            return self.knowledge["age"]
        return "No info found."

    def chat(self, user_input):
        print(f"User: {user_input}")
        
        # Step 1: Reformulate based on history
        standalone_query = self.reformulate_query(user_input)
        if standalone_query != user_input:
            print(f"   (Rewritten Query: '{standalone_query}')")

        # Step 2: Retrieve
        context = self.retrieve(standalone_query)

        # Step 3: Generate
        answer = f"Based on '{context}', here is the answer."
        print(f"AI: {answer}\n")

        # Update history
        self.history.append((user_input, answer))

if __name__ == "__main__":
    bot = MemoryEnhancedRAG()
    bot.chat("Who is the CEO of Google?")
    bot.chat("How old is he?")
