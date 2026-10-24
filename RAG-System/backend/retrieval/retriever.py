from sentence_transformers import SentenceTransformer
import chromadb


class Retriever:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(
            path="chromadb_storage"
        )

        self.collection = self.client.get_collection(
            "research_documents"
        )

    def search(self, query):

        embedding = self.model.encode(query)

        results = self.collection.query(
            query_embeddings=[
                embedding.tolist()
            ],
            n_results=10
        )

        return {
            "documents": results["documents"][0],
            "sources": results["metadatas"][0]
        }
