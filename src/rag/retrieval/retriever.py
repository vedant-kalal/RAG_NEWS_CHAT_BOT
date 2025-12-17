from ...embeddings.vector_store import VectorStoreManager


class Retrieval:
    def __init__(self,vector_store_path):
        self.vector_store = VectorStoreManager(vector_store_path=vector_store_path).create_or_load_vector_store()
        self.retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4}) 
        

    def return_chain(self, query):
        try:
            result_docs = self.retriever.invoke(query)
            return result_docs
        except Exception as e:
            raise RuntimeError(f"Failed to return chain: {str(e)}")
