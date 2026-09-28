from rag.embeddings import EmbeddingService
from rag.vector_store import VectorStore


class ClinicalRetriever:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def retrieve(self, query: str, top_k: int = 3) -> list[dict]:

        query_embedding = self.embedding_service.embed_text(query)

        results = self.vector_store.search(
            query_embedding,
            limit=top_k
        )

        return [
            {
                "text": result.payload["text"],
                "score": result.score
            }
            for result in results
        ]