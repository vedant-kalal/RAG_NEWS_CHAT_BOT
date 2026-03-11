from dotenv import load_dotenv
from ..rag.augmetation.augmentation import Augmentation
from ..rag.generation.generation import Generation
load_dotenv()

class Ai_Response:
    def __init__(self, collection_name="news_chatbot"):
        self.collection_name = collection_name
        self.augmentation = Augmentation(collection_name=collection_name)
        self.generation = Generation()
        self.chain = self.augmentation.augmentation_chain() | self.generation.generation_chain()
    
    def bot_response(self, user_question):
        try:
            return self.chain.invoke(user_question)
        except Exception as e:
            raise RuntimeError(f"Failed to get bot response: {str(e)}")