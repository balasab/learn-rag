from sentence_transformers import CrossEncoder
import chromadb

# 1. Setup
client = chromadb.PersistentClient(path="../02_Intermediate_RAG/chroma_db_data")
collection = client.get_collection("demo_collection")

# Load a Cross-Encoder model designed for re-ranking
# This model takes (query, document) pairs and outputs a relevance score without embeddings.
print("Loading Cross-Encoder model...")
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def retrieve_and_rerank(query, top_k_retrieve=10, top_k_rerank=3):
    print(f"\n--- Processing: '{query}' ---")
    
    # 1. Initial High-Recall Retrieval (fetching more docs than needed)
    results = collection.query(query_texts=[query], n_results=top_k_retrieve)
    retrieved_docs = results["documents"][0]
    
    print(f"Initial Retrieval: {len(retrieved_docs)} documents")
    
    # 2. Re-rank
    # Create pairs of [query, doc]
    pairs = [[query, doc] for doc in retrieved_docs]
    scores = reranker.predict(pairs)
    
    # Sort by re-ranker score
    scored_docs = sorted(list(zip(retrieved_docs, scores)), key=lambda x: x[1], reverse=True)
    
    print(f"Top {top_k_rerank} after Re-ranking:")
    for doc, score in scored_docs[:top_k_rerank]:
        print(f"  Score: {score:.4f} | Content: {doc}")

if __name__ == "__main__":
    retrieve_and_rerank("What is the transformer architecture?")
    # Even if initial retrieval puts "Python" docs high due to some keyword overlap,
    # the re-ranker should push the specific "Transformer" doc to the top.
