import chromadb
from chromadb.utils import embedding_functions

# 1. Connect to the existing DB
client = chromadb.PersistentClient(path="./chroma_db_data")

# 2. Get the collection
collection = client.get_collection(
    name="demo_collection",
    embedding_function=embedding_functions.DefaultEmbeddingFunction()
)

def query_vector_db(query_text, n_results=2):
    print(f"\n--- Querying for: '{query_text}' ---")
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    # Chroma returns lists of lists (one list per query). We only have 1 query.
    for i in range(len(results["ids"][0])):
        doc_id = results["ids"][0][i]
        content = results["documents"][0][i]
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i] # Determine similarity (lower is better for cosine distance in some impls, but Chroma default is distance)
        
        print(f"Result {i+1}:")
        print(f"  ID: {doc_id}")
        print(f"  Content: {content}")
        print(f"  Metadata: {metadata}")
        print(f"  Distance: {distance:.4f}")

if __name__ == "__main__":
    query_vector_db("Tell me about neural networks")
    query_vector_db("What is RAG?")
    query_vector_db("coding languages")
