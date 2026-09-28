from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class VectorStore:

    def __init__(
        self,
        collection_name: str = "clinical_knowledge",
        vector_size: int = 384
    ):
        self.collection_name = collection_name

        self.client = QdrantClient(
            path="data/qdrant"
        )

        self._create_collection(vector_size)

    def _create_collection(self, vector_size: int):
        collections = self.client.get_collections().collections

        if self.collection_name not in [
            collection.name for collection in collections
        ]:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )

    def add_documents(
        self,
        documents: list[str],
        embeddings: list[list[float]]
    ):
        points = []

        for index, (document, embedding) in enumerate(
            zip(documents, embeddings)
        ):
            points.append(
                PointStruct(
                    id=index,
                    vector=embedding,
                    payload={
                        "text": document
                    }
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(
        self,
        query_embedding: list[float],
        limit: int = 3
    ):
        return self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit
        ).points