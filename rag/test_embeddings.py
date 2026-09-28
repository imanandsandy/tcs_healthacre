from rag.ingestion import KnowledgeIngestion


ingestion = KnowledgeIngestion()

count = ingestion.ingest(
    "data/medical_knowledge.json"
)

print(f"\nSuccessfully ingested {count} documents.")