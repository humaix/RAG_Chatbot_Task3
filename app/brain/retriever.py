# using similarityscore 
# class Retriever:
#
#     def __init__(self, vector_store, top_k):
#         self.vector_store = vector_store
#         self.top_k = top_k
#
#     def search(self, question):
#         results = self.vector_store.similarity_search(
#             question,
#             k=self.top_k
#         )
#
#         return results




# using mmr
class Retriever:
    def __init__(self, vector_store, top_k):
        self.retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": top_k,
                "fetch_k": 8,
                "lambda_mult": 0.7
            }
        )
    def search(self, question):
        return self.retriever.invoke(question)
