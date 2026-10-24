from retrieval.pipeline import RetrievalPipeline

pipeline = RetrievalPipeline()

results = pipeline.retrieve(
    "heart disease treatment"
)

print(results)