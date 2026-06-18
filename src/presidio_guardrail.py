from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()


def mask_pii(text: str) -> str:
    """
    Detect and mask PII before sending to LLM.
    """
    results = analyzer.analyze(
        text=text,
        language="en",
    )
    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
    )
    return anonymized.text
