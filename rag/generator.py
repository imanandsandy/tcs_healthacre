import ollama

from backend.core.config import settings


class ClinicalGenerator:

    def __init__(self):
        self.model = settings.OLLAMA_MODEL

    def generate(self, question: str, sources: list[dict]) -> str:

        context = "\n\n".join(
            [
                f"Source {i + 1}:\n{source['text']}"
                for i, source in enumerate(sources)
            ]
        )

        prompt = f"""
You are an evidence-based clinical information assistant.

Answer the user's question using ONLY the provided sources.

STRICT RULES:
- Do not use information outside the provided sources.
- Do not invent facts.
- Do not make a diagnosis.
- Do not prescribe or recommend treatment.
- If the sources do not contain enough information, say:
  "The available sources do not provide enough information to answer this question."
- Clearly identify which source supports each statement.
- This is an information retrieval system, not a replacement for clinical judgment.

SOURCES:
{context}

QUESTION:
{question}

Return a concise answer followed by:

SOURCES USED:
- Source 1
- Source 2
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]