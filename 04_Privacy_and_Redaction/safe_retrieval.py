from presidio_analyzer import AnalyzerEngine
import random

# Scenario: We have retrieved chunks from a DB, but some might accidentally contain raw PII 
# (perhaps they were ingested before the redaction policy was active).
# We must filter them out before sending to the LLM (Safe Retrieval).

analyzer = AnalyzerEngine()

retrieved_chunks = [
    "The project deadline is next Friday.",
    "Please call supervisor at 202-555-0143 to approve the deployment.",
    "RAG systems should ensure data privacy.",
    "Send the report to admin@corp.com immediately."
]

def check_safety(chunks):
    safe_chunks = []
    print("--- Checking retrieved chunks for PII leakage ---")
    
    for chunk in chunks:
        results = analyzer.analyze(text=chunk, entities=["PHONE_NUMBER", "EMAIL_ADDRESS"], language='en')
        
        if results:
            print(f"[BLOCKED] Chunk contains PII: '{chunk}'")
        else:
            print(f"[SAFE]    '{chunk}'")
            safe_chunks.append(chunk)
            
    print(f"\nRetrieved {len(chunks)}, Returning only {len(safe_chunks)} safe chunks.")
    return safe_chunks

if __name__ == "__main__":
    check_safety(retrieved_chunks)
