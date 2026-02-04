"""
01. RAFT (Retrieval-Augmented Fine-Tuning) - Data Prep
======================================================

RAFT is a training recipe to teach LLMs how to perform RAG better.
We cannot fine-tune a model in this script, but we can generate the
TRAINING DATASET structure required for RAFT.

RAFT Dataset Recipe:
For each question, we create training samples with:
1. The Question
2. A list of "Oracle" documents (documents that actually contain the answer)
3. A list of "Distractor" documents (irrelevant docs to teach robustness)
4. Chain of Thought (CoT) reasoning
5. The Final Answer
"""

import random
import json

class RAFTSimulator:
    def __init__(self):
        self.corpus = {
            "doc1": "AlphaCorp's revenue in 2023 was $5B.",
            "doc2": "BetaInc's CEO is Jane Doe.",
            "doc3": "AlphaCorp focuses on AI hardware.",
            "doc4": "GammaLtd makes solar panels."
        }
        
    def generate_dataset_item(self, question, oracle_doc_ids):
        # 1. Get Oracle Docs (The "Truth")
        oracle_docs = [self.corpus[doc_id] for doc_id in oracle_doc_ids]
        
        # 2. Get Distractor Docs (Noise)
        all_ids = list(self.corpus.keys())
        distractor_ids = [did for did in all_ids if did not in oracle_doc_ids]
        distractor_docs = [self.corpus[did] for did in distractor_ids]
        
        # 3. Combine and Shuffle
        context_docs = oracle_docs + distractor_docs
        random.shuffle(context_docs)
        
        # 4. Synthesize Chain of Thought (CoT)
        # In real life, an LLM (GPT-4) generates this part for the training data
        cot_reasoning = (
            f"I need to answer '{question}'. "
            f"Looking at the context, I see a document mentioning '{oracle_docs[0]}'. "
            "Therefore, I can conclude the answer."
        )
        
        return {
            "question": question,
            "context_list": context_docs,
            "cot_thought": cot_reasoning,
            "instruction": "Answer the question based strictly on the context provided."
        }

    def run_demo(self):
        print("--- Generating RAFT Training Data Sample ---\n")
        
        # Sample 1: AlphaCorp Revenue
        item1 = self.generate_dataset_item(
            question="What was AlphaCorp's revenue?",
            oracle_doc_ids=["doc1"]
        )
        
        print("Sample 1 Structure:")
        print(json.dumps(item1, indent=2))
        print("-" * 40)
        
        print("\nNote for User:")
        print("In a real RAFT workflow, you would generate thousands of these samples")
        print("and then fine-tune a Llama-3 or Mistral model specifically on this dataset.")
        print("This teaches the model to ignore the 'Distractor' docs in 'context_list'.")

if __name__ == "__main__":
    sim = RAFTSimulator()
    sim.run_demo()
