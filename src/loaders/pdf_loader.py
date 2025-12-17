import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PDFLoader:
    def __init__(self, chunk_size: int = 600, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", " "]
        )

    def load_pdf(self, pdf_path:str):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File not found: {pdf_path}")

        try:
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
            print("Documents loaded successfully")
            return pages
        except Exception as e:
            raise RuntimeError(f"Failed to load PDF: {str(e)}")

    def split_into_chunks(self,documents):
        try:
            chunks = self.text_splitter.split_documents(documents)
            print(f"Documents split into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            raise RuntimeError(f"Failed to split documents: {str(e)}")

    def process_pdf(self,pdf_path :str):
        print(f"Processing PDF: {pdf_path}")
        documents = self.load_pdf(pdf_path)
        chunks = self.split_into_chunks(documents)
       
        return chunks  