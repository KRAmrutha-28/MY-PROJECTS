from retrieval.reranker import FlashRankReranker

reranker = FlashRankReranker()

passages = [
    "Heart disease affects millions of people.",
    "Python is a programming language.",
    "Treatment for heart disease includes medication.",
    "Cricket is a popular sport."
]

results = reranker.rerank(
    "heart disease treatment",
    passages
)

print(results)