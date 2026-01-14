import chromadb
from chromadb.utils import embedding_functions
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# 1. Setup Retrieval Systems
client = chromadb.PersistentClient(path="../02_Intermediate_RAG/chroma_db_data")
collection = client.get_collection("demo_collection")

# We need the raw documents for BM25 (Keyword search)
# In production, you'd maintain a separate inverted index (Elasticsearch/Solr)
existing_data = collection.get()
documents = existing_data["documents"]
ids = existing_data["ids"]

# 2. Simple Keyword Search (TF-IDF as proxy for BM25)
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

def keyword_search(query, k=5):
    query_vec = vectorizer.transform([query])
    # Dot product for similarity
    scores = (tfidf_matrix * query_vec.T).toarray().flatten()
    # Get top k indices
    top_indices = scores.argsort()[::-1][:k]
    return [(ids[i], scores[i]) for i in top_indices if scores[i] > 0]

def vector_search(query, k=5):
    results = collection.query(query_texts=[query], n_results=k)
    # Chroma returns lists, we simplify
    return [(results["ids"][0][i], 1 - results["distances"][0][i]) for i in range(len(results["ids"][0]))]

def hybrid_search(query, alpha=0.5):
    print(f"\n--- Hybrid Search (Alpha={alpha}) for: '{query}' ---")
    
    # Get results from both basic systems
    kw_results = dict(keyword_search(query, k=5))
    vec_results = dict(vector_search(query, k=5))
    
    # Merge and Normalize scores
    all_ids = set(kw_results.keys()) | set(vec_results.keys())
    final_results = []
    
    for doc_id in all_ids:
        # Simple Weighted Fusion
        # Note: In production, you must normalize scores (e.g., using Reciprocal Rank Fusion - RRF)
        # because BM25 scores are unbounded while Cosine is 0-1.
        kw_score = kw_results.get(doc_id, 0)
        vec_score = vec_results.get(doc_id, 0)
        
        # Simple normalization for demo (assuming TF-IDF is somewhat low range)
        final_score = (alpha * vec_score) + ((1-alpha) * kw_score)
        
        # Retrieve content for display
        idx = ids.index(doc_id)
        content = documents[idx]
        final_results.append((doc_id, content, final_score))
    
    final_results.sort(key=lambda x: x[2], reverse=True)
    
    for res in final_results[:3]:
        print(f"ID: {res[0]} | Score: {res[2]:.3f} | Content: {res[1]}")

if __name__ == "__main__":
    # Query that benefits from keyword match
    hybrid_search("Attention Is All You Need paper", alpha=0.3)
    
    # Query that benefits from semantic match
    hybrid_search("coding tools for AI", alpha=0.7)
