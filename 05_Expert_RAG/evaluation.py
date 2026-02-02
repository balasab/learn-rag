import os
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from ragas.metrics.critique import harmfulness

# NOTE: In a real environment, ensure OPENAI_API_KEY is set
# on os.environ for Ragas/LangChain to work.

def create_evaluation_dataset(data_samples):
    """
    Converts a list of dicts into a HuggingFace Dataset compatible with Ragas.
    Expected keys: 'question', 'answer', 'contexts', 'ground_truth'
    """
    data = {
        'question': [x['question'] for x in data_samples],
        'answer': [x['answer'] for x in data_samples],
        'contexts': [x['contexts'] for x in data_samples],
        'ground_truth': [x['ground_truth'] for x in data_samples]
    }
    return Dataset.from_dict(data)

def evaluate_strategy(strategy_name: str, dataset: Dataset):
    """
    Runs Ragas evaluation on a given dataset for a specific strategy.
    """
    print(f"\n--- Evaluating Strategy: {strategy_name} ---")
    
    # Define metrics to track
    metrics = [
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
        harmfulness
    ]
    
    # Run evaluation
    # raise_exceptions=False prevents crash on individual API failures
    results = evaluate(
        dataset=dataset,
        metrics=metrics,
        raise_exceptions=False
    )
    
    print(f"Results for {strategy_name}:")
    print(results)
    return results

def main():
    # 1. Define Evaluation Data (Golden Dataset)
    # Start with a predefined set of questions and ground truths.
    # In a real scenario, 'contexts' and 'answer' would come from your RAG pipeline.
    
    # Strategy A: Naive RAG (Simulated outputs - retrieval might be noisy)
    strategy_a_samples = [
        {
            "question": "What is Retrieval-Augmented Generation?",
            "answer": "RAG is a method to improve LLM accuracy by retrieving external data.",
            "contexts": [
                "Retrieval-Augmented Generation (RAG) is a technique...",
                "The sky is blue.", # Irrelevant context -> lower precision
            ],
            "ground_truth": "Retrieval-Augmented Generation (RAG) retrieves data to augment generation."
        },
        {
            "question": "How do you install LangChain?",
            "answer": "You can install it using pip or conda.",
            "contexts": [
                "pip install langchain",
                "conda install langchain -c conda-forge"
            ],
            "ground_truth": "Use 'pip install langchain' or 'conda install langchain -c conda-forge'."
        }
    ]

    # Strategy B: Advanced RAG (Simulated outputs - better retrieval & reranking)
    strategy_b_samples = [
        {
            "question": "What is Retrieval-Augmented Generation?",
            "answer": "Retrieval-Augmented Generation (RAG) is an architecture that fetches relevant documents to ground the LLM's answers.",
            "contexts": [
                "Retrieval-Augmented Generation (RAG) is a technique...",
                "It combines parametric and non-parametric memory." # More relevant
            ],
            "ground_truth": "Retrieval-Augmented Generation (RAG) retrieves data to augment generation."
        },
        {
            "question": "How do you install LangChain?",
            "answer": "To install LangChain, run `pip install langchain` or use Conda.",
            "contexts": [
                "pip install langchain",
                "conda install langchain -c conda-forge",
                "Installation guide for LangChain..."
            ],
            "ground_truth": "Use 'pip install langchain' or 'conda install langchain -c conda-forge'."
        }
    ]

    # 2. Convert to Datasets
    ds_a = create_evaluation_dataset(strategy_a_samples)
    ds_b = create_evaluation_dataset(strategy_b_samples)

    # 3. specific RAGAS evaluation logic - Validation
    # NOTE: This step triggers actual LLM calls via Ragas.
    # Ensure you have credits/keys.
    
    try:
        results_a = evaluate_strategy("Naive RAG", ds_a)
        results_b = evaluate_strategy("Advanced RAG + Rerank", ds_b)
        
        # 4. Compare Results
        df_a = results_a.to_pandas()
        df_a['strategy'] = 'Naive RAG'
        
        df_b = results_b.to_pandas()
        df_b['strategy'] = 'Advanced RAG'
        
        comparison_df = pd.concat([df_a, df_b], ignore_index=True)
        print("\n--- Comparative Analysis ---")
        print(comparison_df[['strategy', 'faithfulness', 'answer_relevancy', 'context_precision', 'context_recall']].groupby('strategy').mean())
        
        # Export for visualization/reporting
        comparison_df.to_csv("rag_evaluation_comparison.csv", index=False)
        print("\nDetailed results saved to 'rag_evaluation_comparison.csv'")

    except Exception as e:
        print(f"\n[Error] Ragas evaluation failed (likely due to missing OpenAI Key/Dependencies): {e}")
        print("Please ensure `OPENAI_API_KEY` is exported and `ragas` is installed.")

if __name__ == "__main__":
    main()
