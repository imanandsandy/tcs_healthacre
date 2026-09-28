import json

from rag.embeddings import EmbeddingService
from rag.vector_store import VectorStore


class KnowledgeIngestion:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def load_documents(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def ingest(self, file_path: str):

        documents = self.load_documents(file_path)

        texts = [
            document["text"]
            for document in documents
        ]

        embeddings = self.embedding_service.embed_documents(
            texts
        )

        self.vector_store.add_documents(
            texts,
            embeddings
        )

        return len(documents)