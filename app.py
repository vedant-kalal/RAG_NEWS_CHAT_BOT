import os
import tkinter as tk
from tkinter import filedialog
from src.loaders.pdf_loader import PDFLoader 
from src.embeddings.vector_store import VectorStoreManager
from src.chat_bot.chat_bot_design import ChatBot
from src.embeddings.vector_db import create_tables, is_pdf_loaded, add_pdf_record
from dotenv import load_dotenv

load_dotenv()
create_tables()

def select_pdf_file():
    root = tk.Tk()
    root.withdraw() 
    root.attributes('-topmost', True) 
    
    file_path = filedialog.askopenfilename(
        title="Select PDF File",
        filetypes=[("PDF Files", "*.pdf")]
    )
    root.destroy()
    return file_path

def get_unique_pdf_name(pdf_path):
    import hashlib
    pdf_name = os.path.basename(pdf_path)
    clean_name = pdf_name.replace(".", "_")
    path_hash = hashlib.md5(os.path.abspath(pdf_path).encode()).hexdigest()[:8]
    return f"{clean_name}_{path_hash}"

def main():
    while True:
        print("\nChoose an option:")
        print("1. ADD NEW PDF")
        print("2. CHAT WITH PDF")
        print("3. EXIT")

        option = input("Enter your choice: ")
        
        if option == "1":
            print("Please select a PDF file from the dialog window...")
            pdf_path = select_pdf_file()
            if not pdf_path:
                print("No file selected.")
                continue
            
            print(f"Selected: {pdf_path}")
            
            unique_name = get_unique_pdf_name(pdf_path)
            
            if is_pdf_loaded(unique_name):
                print(f"'{os.path.basename(pdf_path)}' is already loaded in the database. Skipping processing.")
            else:
                pdf_loader = PDFLoader()
                documents = pdf_loader.process_pdf(pdf_path)
                
                print(f"Creating vector store collection: {unique_name}")
                vector_store_manager = VectorStoreManager(collection_name=unique_name)
                vector_store_manager.process_documents(documents)
                add_pdf_record(unique_name)
                print("PDF loaded and vector store created successfully!")

        elif option == "2":
            print("Please select the PDF file you want to chat with...")
            pdf_path = select_pdf_file()
            if not pdf_path:
                print("No file selected.")
                continue

            unique_name = get_unique_pdf_name(pdf_path)
            
            if is_pdf_loaded(unique_name):
                chatbot = ChatBot(collection_name=unique_name)
                chatbot.Run_ChatBot()
            else:
                print(f"No vector store found for this PDF. Please upload it first using Option 1.")
        
        elif option == "3":
            print("Exiting...")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
