from typing import List

# Mocking an LLM for Query Expansion to avoid API keys in this demo code.
def ask_llm(prompt):
    # In reality: return openai.chat.completions.create(...)
    if "machine learning" in prompt.lower():
        return "1. What is ML?\n2. Deep Learning vs Machine Learning\n3. AI algorithms"
    if "rag" in prompt.lower():
        return "1. Retrieval Augmented Generation\n2. improving LLMs with external data\n3. vector database search"
    return "1. general query\n2. search help"

def generate_sub_queries(original_query: str) -> List[str]:
    print(f"Generating sub-queries for: '{original_query}'")
    
    prompt = f"Generate 3 diverse search queries based on: {original_query}"
    response = ask_llm(prompt)
    
    # Basic parsing
    sub_queries = [line.strip().split('. ')[1] for line in response.split('\n') if '. ' in line]
    if not sub_queries:
        sub_queries = [original_query]
        
    print(f"Generated: {sub_queries}")
    return sub_queries

# In a real pipeline, you would retrieve documents for ALL these queries
# and use Reciprocal Rank Fusion (RRF) to de-duplicate and rank them.

if __name__ == "__main__":
    generate_sub_queries("Tell me about RAG concepts")
