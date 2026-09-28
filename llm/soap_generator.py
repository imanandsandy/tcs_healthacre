import json
import ollama

from backend.core.config import settings
from schemas.soap import SOAPNote


class SOAPGenerator:

    def __init__(self):
        self.model = settings.OLLAMA_MODEL

    def generate(self, transcript: str) -> SOAPNote:

        prompt = f"""
You are a clinical documentation assistant.

Convert the provided sanitized doctor-patient conversation
into a structured SOAP note.

STRICT RULES:
- Use ONLY information explicitly stated in the conversation.
- NEVER infer, assume, diagnose, or speculate.
- NEVER invent symptoms, medications, allergies, history,
  examination findings, vital signs, investigations, or treatment.
- If information is missing, write "Not mentioned."
- Do not provide medical advice.
- Do not add information from your general medical knowledge.

Return ONLY valid JSON.

Required format:

{{
  "subjective": "...",
  "objective": "...",
  "assessment": "...",
  "plan": "..."
}}

SANITIZED CONVERSATION:
{transcript}
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

        content = response["message"]["content"]

        data = json.loads(content)

        return SOAPNote(**data)