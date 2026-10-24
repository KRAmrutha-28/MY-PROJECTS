from retrieval.retriever import Retriever


class RAGService:

    def __init__(self):

        self.retriever = Retriever()

    def search(self, query):

        results = self.retriever.retrieve(query)

        return {
            "query": query,
            "results": results
        }