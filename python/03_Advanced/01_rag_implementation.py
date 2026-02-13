import asyncio
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Protocol, Dict, Optional, Any
from enum import Enum

# --- Domain Models ---

@dataclass(frozen=True)
class Document:
    """Represents a piece of text content with metadata."""
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(random.randint(1000, 9999)))

@dataclass
class SearchResult:
    document: Document
    score: float

class ModelType(Enum):
    EMBEDDING = "embedding"
    LLM = "llm"

# --- Interfaces (Protocols) ---
# Using Protocols allows for structural subtyping (duck typing) which is very pythonic yet type-safe.

class EmbeddingModel(Protocol):
    async def embed_query(self, text: str) -> List[float]:
        ...
    
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        ...

class VectorStore(Protocol):
    async def add_documents(self, documents: List[Document]) -> None:
        ...

    async def similarity_search(self, query_vector: List[float], k: int = 4) -> List[SearchResult]:
        ...

class LLM(Protocol):
    async def generate(self, prompt: str) -> str:
        ...

# --- Implementations ---

class MockEmbeddingModel:
    """Simulates an embedding model by returning random vectors."""
    def __init__(self, start_dim: int = 768):
        self.dim = start_dim

    async def embed_query(self, text: str) -> List[float]:
        await asyncio.sleep(0.1) # Simulate network latency
        return [random.random() for _ in range(self.dim)]

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        await asyncio.sleep(0.2)
        return [[random.random() for _ in range(self.dim)] for _ in texts]

class MockVectorStore:
    """In-memory vector store simulation."""
    def __init__(self):
        self.store: Dict[str, Document] = {}
        self.vectors: Dict[str, List[float]] = {} # id -> vector

    async def add_documents(self, documents: List[Document], vectors: Optional[List[List[float]]] = None) -> None:
        # In a real scenario, vectors would be computed here or passed in.
        # simulating generic vectors if not provided for the sake of the interface
        for idx, doc in enumerate(documents):
            self.store[doc.id] = doc
            self.vectors[doc.id] = vectors[idx] if vectors else [random.random() for _ in range(768)]
        print(f"Stored {len(documents)} documents.")

    async def similarity_search(self, query_vector: List[float], k: int = 4) -> List[SearchResult]:
        await asyncio.sleep(0.1) # Simulate index search
        # Return random documents as "sorted" results
        docs = list(self.store.values())
        k = min(k, len(docs))
        selected = random.sample(docs, k)
        return [SearchResult(document=doc, score=random.uniform(0.7, 0.99)) for doc in selected]

class MockLLM:
    async def generate(self, prompt: str) -> str:
        print(f"Thinking on prompt: {prompt[:50]}...")
        await asyncio.sleep(1.0) # Simulate generation time
        return f"GenAI Response based on context. (Simulated output for length {len(prompt)})"

# --- RAG Orchestrator ---

class RAGPipeline:
    """
    Orchestrates the Retrieval Augmented Generation process.
    Demonstrates Dependency Injection via constructor.
    """
    def __init__(self, embedder: EmbeddingModel, vector_store: VectorStore, llm: LLM):
        self.embedder = embedder
        self.vector_store = vector_store
        self.llm = llm

    async def ingest(self, documents: List[Document]):
        print("--- Ingestion Step ---")
        texts = [d.content for d in documents]
        embeddings = await self.embedder.embed_documents(texts)
        await self.vector_store.add_documents(documents, vectors=embeddings)

    async def query(self, user_query: str) -> str:
        print(f"\n--- Querying: '{user_query}' ---")
        
        # 1. Embed Query
        query_vec = await self.embedder.embed_query(user_query)
        
        # 2. Retrieve
        results = await self.vector_store.similarity_search(query_vec, k=3)
        print(f"Retrieved {len(results)} relevant documents.")
        
        # 3. Construct Context
        context_str = "\n\n".join([r.document.content for r in results])
        
        # 4. Augment Prompt
        final_prompt = f"""
        Use the following context to answer the question.
        
        Context:
        {context_str}
        
        Question: {user_query}
        """
        
        # 5. Generate
        response = await self.llm.generate(final_prompt)
        return response

# --- Application Entry Point ---

async def main():
    # 1. Setup Dependencies
    embedder = MockEmbeddingModel()
    store = MockVectorStore()
    llm = MockLLM()
    
    pipeline = RAGPipeline(embedder, store, llm)
    
    # 2. Ingest Data
    knowledge_base = [
        Document(content="Python is dynamically typed.", metadata={"topic": "python"}),
        Document(content="Asyncio is used for concurrent execution.", metadata={"topic": "async"}),
        Document(content="RAG combines retrieval with generation.", metadata={"topic": "ai"}),
        Document(content="Decorators modify function behavior.", metadata={"topic": "python"}),
    ]
    
    await pipeline.ingest(knowledge_base)
    
    # 3. Run Query
    answer = await pipeline.query("How does RAG work together with Python?")
    print(f"\nFinal Answer:\n{answer}")

if __name__ == "__main__":
    asyncio.run(main())
