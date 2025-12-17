from ...llm.model_loader import load_model
from langchain_core.output_parsers import StrOutputParser

class Generation:
    def __init__(self):
        self.parser = StrOutputParser()
    
    def generation_chain(self):
        try:
            second_chain = load_model() | self.parser
            return second_chain
        except Exception as e:
            raise RuntimeError(f"Failed to create generation chain: {str(e)}")
    
    
