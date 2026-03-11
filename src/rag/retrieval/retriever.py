from ...embeddings.vector_store import VectorStoreManager


class Retrieval:
    def __init__(self, collection_name="news_chatbot"):
        self.vector_store = VectorStoreManager(collection_name=collection_name).create_or_load_vector_store()
        self.retriever = self.vector_store.as_retriever(search_type="mmr",search_kwargs={"k": 4, "fetch_k": 20}) 
        

    def return_chain(self, query):
        try:
            result_docs = self.retriever.invoke(query)
            return result_docs
        except Exception as e:
            raise RuntimeError(f"Failed to return chain: {str(e)}")
