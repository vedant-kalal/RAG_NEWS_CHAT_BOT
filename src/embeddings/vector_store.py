from langchain_chroma import Chroma
from ..llm.model_loader import load_embedding_model
import os

class VectorStoreManager:
    def __init__(self, vector_store_path: str):
        self.vector_store_path = vector_store_path
        self.embedding_model = load_embedding_model()
        
    
    def create_or_load_vector_store(self):
        try:
            vector_store = Chroma(embedding_function=self.embedding_model, persist_directory=self.vector_store_path)
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
            documents = vector_store.get(include=["embeddings"])
            print("-" * 50)
            print("Documents retrieved successfully")
            print("-" * 50)
            print(documents)
            print("-" * 50)
            return documents
        except Exception as e:
            raise RuntimeError(f"Failed to  retrieve documents: {str(e)}")


    def delete_vector_store(self, vector_store):
        try:
            vector_store.delete()
            print("-" * 50)
            print("Vector store deleted successfully")
            print("-" * 50)
            return vector_store
        except Exception as e:
            raise RuntimeError(f"Failed to delete vector store: {str(e)}")
    
    def delete_document(self, vector_store, document_id):
        try:
            vector_store.delete(document_id=document_id)
            print("-" * 50)
            print("Document deleted successfully")
            print("-" * 50)
            return vector_store
        except Exception as e:
            raise RuntimeError(f"Failed to delete document: {str(e)}")

    def update_document(self, vector_store, document_id, document):
        try:
            vector_store.update_document(document_id=document_id, document=document)
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