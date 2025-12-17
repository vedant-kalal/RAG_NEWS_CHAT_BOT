import os
import tkinter as tk
from tkinter import filedialog
from src.loaders.pdf_loader import PDFLoader 
from src.embeddings.vector_store import VectorStoreManager
from src.chat_bot.chat_bot_design import ChatBot

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

def get_vector_store_path(pdf_name):

    clean_name = pdf_name.replace(".", "_") + "_db"
    return os.path.join("data", "embeddings_db", clean_name)

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
            pdf_loader = PDFLoader()
            documents = pdf_loader.process_pdf(pdf_path)
            
            pdf_name = os.path.basename(pdf_path)
            vector_store_path = get_vector_store_path(pdf_name)
            
            print(f"Creating vector store at: {vector_store_path}")
            vector_store_manager = VectorStoreManager(vector_store_path=vector_store_path)
            vector_store_manager.process_documents(documents)
            print("PDF loaded and vector store created successfully!")

        elif option == "2":
            pdf_name = input("Enter the name of the PDF (e.g., sample.pdf): ")
            vector_store_path = get_vector_store_path(pdf_name)
            
            if os.path.exists(vector_store_path):
                chatbot = ChatBot(vector_store_path=vector_store_path)
                chatbot.Run_ChatBot()
            else:
                print(f"No vector store found for '{pdf_name}' at '{vector_store_path}'.")
                print("Please upload the PDF first using Option 1.")
        
        elif option == "3":
            print("Exiting...")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
