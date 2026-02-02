import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import MarkdownHeaderTextSplitter
import uuid

# 1. Simulate a Document with Structure (Layout)
# In a real scenario, this might come from a PDF parser that detects headers/sections.
# We use Markdown here as a proxy for structural layout.
markdown_document = """
# Employee Handbook

## 1. Leave Policy
Employees are entitled to 20 days of paid leave per year.
Sick leave is separate and grants 10 days per year.

## 2. Remote Work
### 2.1 Eligibility
Employees must have completed their probation period to be eligible for remote work.

### 2.2 Equipment
The company will provide a laptop and monitor for remote workers.

## 3. Code of Conduct
Respect your colleagues. Harassment of any kind is not tolerated.
"""

print("--- 1. Document Structure ---")
print(markdown_document)

# 2. Layout-Aware Parsing
# We split based on headers. This attaches the "context" (Header) to the chunk metadata.
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_header_splits = markdown_splitter.split_text(markdown_document)

print(f"\n--- 2. Split Chunks (Layout Aware) ---")
for split in md_header_splits:
    print(f"Content: {split.page_content}")
    print(f"Metadata: {split.metadata}")
    print("-" * 20)

# 3. Ingest into ChromaDB with Metadata
client = chromadb.PersistentClient(path="./chroma_db_layout_test")
collection_name = "policy_collection"

# Cleanup
try:
    client.delete_collection(name=collection_name)
except:
    pass

collection = client.create_collection(name=collection_name)

documents = [split.page_content for split in md_header_splits]
metadatas = [split.metadata for split in md_header_splits]
ids = [str(uuid.uuid4()) for _ in md_header_splits]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)
print("\n--- 3. Ingestion Complete ---")

# 4. Query with Metadata Filtering
# Scenario: User specifically asks about Remote Work equipment.
# We can filter search space to only look at chunks under 'Remote Work'.

query = "What equipment do I get?"
print(f"\n--- 4. Query: '{query}' ---")

# Search without filter
results_no_filter = collection.query(
    query_texts=[query],
    n_results=1
)
print(f"Top Result (No Filter): {results_no_filter['documents'][0][0]}")

# Search WITH filter (Metadata Filtering)
# We only want chunks that belong to "Header 2": "2. Remote Work"
# This reduces hallucinations from other sections (e.g., if code of conduct mentioned equipment)
results_with_filter = collection.query(
    query_texts=[query],
    n_results=1,
    where={"Header 2": "2. Remote Work"}
)
print(f"Top Result (With Filter 'Remote Work'): {results_with_filter['documents'][0][0]}")

# Demonstrating a filter that might exclude the answer to prove it works
results_wrong_filter = collection.query(
    query_texts=[query],
    n_results=1,
    where={"Header 2": "1. Leave Policy"}
)
# This might return nothing or a less relevant match depending on collection size,
# but it proves we are constrained to the wrong section.
print(f"Top Result (With Filter 'Leave Policy'): {results_wrong_filter['documents'][0][0] if results_wrong_filter['documents'][0] else 'No match'}")
