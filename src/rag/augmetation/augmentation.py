from ...llm.model_loader import load_model
from langchain_core.prompts import PromptTemplate
from ..retrieval.retriever import Retrieval
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

chat_history = []

class Augmentation:
    def __init__(self, collection_name="news_chatbot"):
        self.model = load_model()
        self.retriever = Retrieval(collection_name=collection_name).retriever
        self.chat_history = chat_history

        self.prompt_template = ChatPromptTemplate.from_messages([

            ("system",
                """
        You are a helpful NEWS CHATBOT. You can engage in normal conversation (like greetings or answering "who are you").
        When the user asks questions about specific topics, theories, or facts, answer based ONLY on the provided news PDF context.

        Follow these STRICT rules:

        1) First analyze the answer extracted from the context.
        - Fix grammatical mistakes.
        - Fix spelling errors.
        - Format the answer cleanly.

        2) If the user's question is a factual inquiry and the answer is NOT present in the context, reply with exactly one of these:
        - "I don't know"
        - "I am not sure"
        - "Topic related to '{question}' is not available in the context"

        3) If the user is just saying hi or asking general conversational questions, you MAY answer them naturally without relying on the context.

        4) Provide the answer **directly**.  
        DO NOT write phrases like:
        - "According to the context"
        - "Based on the given information"

        5) Never reveal your thoughts or reasoning.  
        Never justify how you found the answer.

        6) Final output format:
        ANSWER :- "<your answer>"
        """
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human",
                """
        CONTEXT:
        {context}

        QUESTION:
        {question}

        Provide the answer following all rules.
        """
            )
        ])

    def format_docs(self, docs):
        try:
            documents = "\n\n".join(doc.page_content for doc in docs)
            return documents
        except Exception as e:
            raise RuntimeError(f"Failed to format documents: {str(e)}")

    def final_parallel_chain(self):
        try:
            parallel_chain = RunnableParallel(
                {
                    "context": self.retriever | self.format_docs,
                    "question": RunnablePassthrough(),
                    "chat_history": lambda x: self.chat_history
                }
            )
            return parallel_chain
        except Exception as e:
            raise RuntimeError(f"Failed to create parallel chain: {str(e)}")

    def augmentation_chain(self):
        try:
            first_chain = self.final_parallel_chain() | self.prompt_template 
            return first_chain
        except Exception as e:
            raise RuntimeError(f"Failed to create augmentation chain: {str(e)}")
        