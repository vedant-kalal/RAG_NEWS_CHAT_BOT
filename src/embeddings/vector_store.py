from langchain_chroma import Chroma
from ..llm.model_loader import load_embedding_model
import os
from langchain_community.vectorstores import PGVector

COLLECTION_NAME = "news_chatbot"
CONNECTION_STRING = os.getenv("DATABASE_URL")

class VectorStoreManager:
    def __init__(self, collection_name=COLLECTION_NAME):
        self.embedding_model = load_embedding_model()
        self.collection_name = collection_name
        self.connection_string = CONNECTION_STRING
        
    
    def create_or_load_vector_store(self):
        try:
            vector_store = PGVector(
                collection_name=self.collection_name,
                connection_string=self.connection_string,
                embedding_function=self.embedding_model,
                distance_strategy="cosine"
            )

            return vector_store
        except Exception as e:
            raise RuntimeError(f"Failed to create/load vector store: {str(e)}")

    def add_documents(self, vector_store, documents):
        try:
            vector_store.add_documents(documents)
            print("-" * 50)
            print("Documents added to vector store successfully")
            print("-" * 50)
            return vector_store
        except Exception as e:
            raise RuntimeError(f"Failed to add documents to vector store: {str(e)}")    


    def get_all_documents(self, vector_store):
        try:
            # PGVector doesn't support .get()
            documents = vector_store.similarity_search("", k=1000)

            print("-" * 50)
            print("Documents retrieved successfully")
            print("-" * 50)
            print(documents)
            print("-" * 50)

            return documents

        except Exception as e:
            raise RuntimeError(f"Failed to retrieve documents: {str(e)}")


    def delete_vector_store(self, vector_store):
        try:
            # deletes the entire collection
            vector_store.delete_collection()

            print("-" * 50)
            print("Vector store deleted successfully")
            print("-" * 50)

            return vector_store

        except Exception as e:
            raise RuntimeError(f"Failed to delete vector store: {str(e)}")


    def delete_document(self, vector_store, document_id):
        try:
            vector_store.delete(ids=[document_id])

            print("-" * 50)
            print("Document deleted successfully")
            print("-" * 50)

            return vector_store

        except Exception as e:
            raise RuntimeError(f"Failed to delete document: {str(e)}")


    def update_document(self, vector_store, document_id, document):
        try:
            # PGVector doesn't support update directly
            vector_store.delete(ids=[document_id])
            vector_store.add_documents([document])

            print("-" * 50)
            print("Document updated successfully")
            print("-" * 50)

            return vector_store

        except Exception as e:
            raise RuntimeError(f"Failed to update document: {str(e)}")


    def process_documents(self, documents):
        try:
            vector_store = self.create_or_load_vector_store()
            vector_store = self.add_documents(vector_store, documents)

            print("-" * 50)
            print("Documents processed successfully")
            print("-" * 50)

            return vector_store

        except Exception as e:
            raise RuntimeError(f"Failed Execution: {str(e)}")