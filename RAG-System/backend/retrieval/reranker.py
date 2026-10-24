from flashrank import Ranker, RerankRequest

ranker = Ranker()


def rerank_chunks(query, chunks):

    passages = []

    for i, chunk in enumerate(chunks):

        passages.append({
            "id": i,
            "text": chunk
        })

    rerank_request = RerankRequest(
        query=query,
        passages=passages
    )

    results = ranker.rerank(
        rerank_request
    )

    return [
        item["text"]
        for item in results[:5]
    ]