import chromadb
from chromadb.utils import embedding_functions


class RAGService:
    def __init__(self, ollama_api_url: str, gemini_api_key: str):
        self.chroma_client = chromadb.Client()
        self.ollama_ef = embedding_functions.OllamaEmbeddingFunction(
            url=f"{ollama_api_url}/api/embeddings",
            model_name="all-minilm:latest",
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name="project_data", embedding_function=self.ollama_ef
        )

    def ingest_document(self, document: str, metadata: dict):
        self.collection.add(
            documents=[document],
            metadatas=[metadata],
            ids=[str(metadata.get("id", hash(document)))],
        )

    def query(self, query_text: str, n_results: int = 5):
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
        )
