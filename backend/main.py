from fastapi import FastAPI
import ollama

from backend.core.config import settings

app = FastAPI(
    title="Healthcare AI Assistant",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "message": "Healthcare AI Assistant API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/llm-test")
def llm_test():
    response = ollama.chat(
        model=settings.OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": "Explain SOAP notes in healthcare in 2 sentences."
            }
        ]
    )

    return {
        "model": settings.OLLAMA_MODEL,
        "response": response["message"]["content"]
    }