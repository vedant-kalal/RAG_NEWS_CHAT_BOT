from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace,HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()   


def load_model():
    model = ChatGroq(
        model="openai/gpt-oss-120b", 
        temperature=0,
    )
    return model

def load_embedding_model():
    embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    )
    return embedding_model