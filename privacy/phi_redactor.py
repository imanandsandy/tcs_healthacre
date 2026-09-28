from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


class PHIRedactor:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def redact(self, text: str) -> str:
        results = self.analyzer.analyze(
            text=text,
            language="en"
        )

        anonymized = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )

        return anonymized.text