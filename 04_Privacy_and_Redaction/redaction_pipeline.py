from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Prerequisite:
# python -m spacy download en_core_web_lg
# Code handles the missing model gracefully-ish, but user should install it.

try:
    analyzer = AnalyzerEngine()
except OSError:
    print("Spacy model not found. Please run: python -m spacy download en_core_web_lg")
    exit(1)
    
anonymizer = AnonymizerEngine()

def redact_text(text: str):
    print(f"\nOriginal: {text}")
    
    # 1. Analyze (Detect PII)
    results = analyzer.analyze(text=text, entities=["PHONE_NUMBER", "EMAIL_ADDRESS", "PERSON"], language='en')
    print(f"Detected {len(results)} PII entities.")
    
    # 2. Anonymize (Redact)
    # Define how to replace specific entities
    operators = {
        "PERSON": OperatorConfig("replace", {"new_value": "<PERSON>"}),
        "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<PHONE_REDACTED>"}),
        "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "<EMAIL_REDACTED>"}),
    }
    
    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators=operators
    )
    
    print(f"Redacted: {anonymized_result.text}")
    return anonymized_result.text

if __name__ == "__main__":
    # Example 1
    redact_text("Contact John Doe at 555-0199 or via email john.doe@example.com for the secret codes.")
    
    # Example 2
    redact_text("The patient Alice Smith was admitted on Monday.")
