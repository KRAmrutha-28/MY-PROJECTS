from retrieval.retriever import Retriever
from retrieval.reranker import rerank_chunks


class RetrievalPipeline:

    def __init__(self):
        self.retriever = Retriever()

    def retrieve(self, query):

        results = self.retriever.search(query)

        documents = results["documents"]

        print("\n====================")
        print("Retrieved Chunks:", len(documents))
        print("====================")

        ranked_chunks = rerank_chunks(
            query,
            documents
        )

        print("After FlashRank:", len(ranked_chunks))
        print("====================\n")

        return ranked_chunks