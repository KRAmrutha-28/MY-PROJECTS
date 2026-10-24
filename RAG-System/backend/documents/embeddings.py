from sentence_transformers import SentenceTransformer
import chromadb
import uuid


class EmbeddingManager:

    def __init__(self):

        print("Loading Sentence Transformer...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Connecting to ChromaDB...")

        self.client = chromadb.PersistentClient(
            path="chromadb_storage"
        )

        self.collection = self.client.get_or_create_collection(
            name="research_documents"
        )

        print("ChromaDB collection ready.")

    def store_chunks(
        self,
        chunks,
        source_name
    ):

        print("=================================")
        print("Chunks received:", len(chunks))
        print("=================================")

        if not chunks:

            raise Exception(
                "No chunks generated from document"
            )

        print(
            "Generating embeddings..."
        )

        embeddings = self.model.encode(
            chunks,
            show_progress_bar=True
        )

        print(
            "Embeddings generated:",
            len(embeddings)
        )

        ids = [
            str(uuid.uuid4())
            for _ in chunks
        ]

        print(
            "IDs generated:",
            len(ids)
        )

        metadatas = [
            {
                "source": source_name
            }
            for _ in chunks
        ]

        BATCH_SIZE = 500

        total_batches = (
            len(chunks) + BATCH_SIZE - 1
        ) // BATCH_SIZE

        print(
            f"Storing in {total_batches} batches..."
        )

        for i in range(
            0,
            len(chunks),
            BATCH_SIZE
        ):

            batch_chunks = chunks[
                i:i + BATCH_SIZE
            ]

            batch_embeddings = embeddings[
                i:i + BATCH_SIZE
            ]

            batch_ids = ids[
                i:i + BATCH_SIZE
            ]

            batch_metadatas = metadatas[
                i:i + BATCH_SIZE
            ]

            self.collection.add(
                ids=batch_ids,
                documents=batch_chunks,
                embeddings=batch_embeddings.tolist(),
                metadatas=batch_metadatas
            )

            batch_number = (
                i // BATCH_SIZE
            ) + 1

            print(
                f"Stored Batch "
                f"{batch_number}/{total_batches}"
            )

        print(
            "================================="
        )
        print(
            "Stored successfully in ChromaDB"
        )
        print(
            "================================="
        )

        return len(chunks)

    def delete_document_chunks(
        self,
        source_name
    ):

        try:

            print(
                f"Deleting ChromaDB chunks for: {source_name}"
            )

            self.collection.delete(
                where={
                    "source": source_name
                }
            )

            print(
                f"Successfully deleted chunks for: {source_name}"
            )

            return True

        except Exception as e:

            print(
                "ChromaDB delete error:",
                str(e)
            )

            return False

    def get_collection_count(self):

        try:

            count = self.collection.count()

            print(
                f"Total vectors in ChromaDB: {count}"
            )

            return count

        except Exception as e:

            print(
                "Count error:",
                str(e)
            )

            return 0