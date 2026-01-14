import math
from typing import List, Dict

# 1. Knowledge Base (The "Retrieval" Source)
# In a real app, this would be a Vector Database (Chroma, Pinecone, etc.)
# Here we use a simple list of strings for demonstration.
knowledge_base = [
    {"id": 1, "content": "RAG stands for Retrieval-Augmented Generation."},
    {"id": 2, "content": "RAG combines a retriever system with a generative model."},
    {"id": 3, "content": "The retriever finds relevant documents based on the user query."},
    {"id": 4, "content": "The generator produces an answer using the retrieved context."},
    {"id": 5, "content": "Fine-tuning updates the model's weights, while RAG provides external knowledge."},
    {"id": 6, "content": "Vector embeddings are often used to measure similarity between query and documents."}
]

# 2. Simple Similarity Function (The "Retriever" Logic)
# In a real app, this would use Cosine Similarity on Vector Embeddings.
# Here we use a naive keyword matching approach for simplicity.
def retrieve_documents(query: str, top_k: int = 2) -> List[Dict]:
    print(f"\n--- Retrieving relevant info for: '{query}' ---")
    
    # Simple scoring: count how many words from query appear in the content
    scored_docs = []
    import string
    
    def normalize_tokens(text: str) -> set:
        # Standardize matching: lower case, remove punctuation
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        return set(text.split())

    query_words = normalize_tokens(query)
    
    for doc in knowledge_base:
        doc_words = normalize_tokens(doc["content"])
        # Jaccard similarity-ish (intersection count)
        score = len(query_words.intersection(doc_words))
        scored_docs.append((doc, score))
    
    # Sort by score (descending) and take top_k
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    
    # Filter out 0 scores (irrelevant)
    relevant_docs = [doc for doc, score in scored_docs if score > 0]
    
    return relevant_docs[:top_k]

# 3. Simple Generator (The "Generation" Logic)
# In a real app, this would be an LLM call (e.g., OpenAI GPT-4, Llama 3).
# Here we mock the generation by filling a template.
def generate_answer(query: str, context_docs: List[Dict]) -> str:
    print(f"--- Generating answer ---")
    
    if not context_docs:
        return "I don't have enough information to answer that."
    
    # Combine content from retrieved docs
    context_text = "\n".join([f"- {d['content']}" for d in context_docs])
    
    # Mock LLM prompt structure
    prompt = f"""
    [System]: You are a helpful assistant. Answer the user info using ONLY the context provided.
    
    [User Query]: {query}
    
    [Context]:
    {context_text}
    
    [Answer]: (Simulated LLM Output based on context above)
    """
    
    # In a real script, you'd do: response = openai.chat.completions.create(...)
    # Here we just return a clear message showing what happened.
    return f"Based on the context:\n{context_text}\n\nI can tell you that {query.replace('?', '')} involves using retrieved docs to inform the answer."

# 4. Main RAG Pipeline
def run_rag_pipeline(query: str):
    # Step 1: Retrieve
    retrieved_docs = retrieve_documents(query, top_k=2)
    print(f"Retrieved {len(retrieved_docs)} documents.")
    
    # Step 2: Generate
    answer = generate_answer(query, retrieved_docs)
    
    print(f"\n[Final Answer]: {answer}\n")

if __name__ == "__main__":
    # Test queries
    run_rag_pipeline("What is RAG?")
    run_rag_pipeline("How does the retriever work?")
    run_rag_pipeline("Tell me about fine-tuning vs RAG")
