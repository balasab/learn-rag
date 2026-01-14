import chromadb
from chromadb.utils import embedding_functions
import os

# 1. Setup ChromaDB client
# This creates a persistent database on disk in the 'chroma_db_data' folder
client = chromadb.PersistentClient(path="./chroma_db_data")

# 2. Define an Embedding Function
# We use the default Sentence Transformer model (all-MiniLM-L6-v2) built into Chroma
# In production, you might use OpenAIEmbeddingFunction or similar.
default_ef = embedding_functions.DefaultEmbeddingFunction()

# 3. Create or Get a Collection
# A collection is like a table in SQL.
collection_name = "demo_collection"
try:
    client.delete_collection(name=collection_name) # Cleanup for fresh run
    print(f"Deleted existing collection: {collection_name}")
except:
    pass

collection = client.create_collection(
    name=collection_name,
    embedding_function=default_ef,
    metadata={"hnsw:space": "cosine"} # Similarity metric
)

# 4. Mock Data Ingestion
# In a real app, this would come from PDF loaders (pypdf) or web scrapers.
documents = [
    "Machine learning is a field of inquiry devoted to understanding and building methods that 'learn'.",
    "Deep learning is part of a broader family of machine learning methods based on artificial neural networks.",
    "Retrieval-augmented generation (RAG) is a technique that grants LLMs access to external data.",
    "Python is a high-level, general-purpose programming language.",
    "The transformer architecture was introduced in the paper 'Attention Is All You Need'."
]

metadatas = [
    {"source": "wiki_ml", "category": "AI"},
    {"source": "wiki_dl", "category": "AI"},
    {"source": "tech_blog", "category": "RAG"},
    {"source": "wiki_python", "category": "Programming"},
    {"source": "paper_2017", "category": "AI"}
]

ids = [f"doc_{i}" for i in range(len(documents))]

print(f"Adding {len(documents)} documents to the vector store...")
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print(f"Ingestion complete. Collection count: {collection.count()}")
