from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace,HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()   


def load_llm():
    llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=0.4,
    )
    return llm

def load_model():
    model = ChatHuggingFace(llm = load_llm())
    return model

def load_embedding_model():
    embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    )
    return embedding_model