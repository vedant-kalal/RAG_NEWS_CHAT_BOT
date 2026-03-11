from .AI_Response import Ai_Response
from ..rag.augmetation.augmentation import Augmentation,chat_history
import halo
from datetime import datetime
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


class ChatBot:
    def __init__(self, collection_name="news_chatbot"):
        self.collection_name = collection_name
        self.chat_history = chat_history
        self.user_chat_history = []
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ai_response = Ai_Response(collection_name=collection_name)
    
    def Run_ChatBot(self):
        try:
            self.user_chat_history.append("\n" +"---------------------- NEW CONVERSATION STARTED ---------------------- TIME:- " + self.current_time + "\n")
            starting_line = "-----------------HELLO, WELCOME TO NEWS CHATBOT , TYPE:- 'exit' TO EXIT THE CHATBOT-----------------"
            self.user_chat_history.append("\n" + "AI: " + starting_line + "\n")

            self.chat_history.append(SystemMessage(content=starting_line))
            print("\n" + starting_line + "\n")
            while True:
                user_input = input("User: ")
                
                
                if user_input.lower() == "exit":
                    print("\n" + "----------------THANK YOU FOR USING THE CHATBOT----------------" + "\n")
                    self.user_chat_history.append("\n" + "AI: " + "THANK YOU FOR USING THE CHATBOT" + "\n")
                    self.user_chat_history.append("\n" + "---------------------- CONVERSATION ENDED ----------------------"+ self.current_time + "\n")
                    with open("data/chat_history/chat_history.txt", "w") as f:
                        f.write("\n".join(self.user_chat_history))
                    self.user_chat_history.clear()
                    self.chat_history.clear()
                    break
                    
                else:
                    with halo.Halo("Thinking..."):
                        ai_response = self.ai_response.bot_response(user_question=user_input)

                    print("\n" + "AI: " + ai_response + "\n")
                    self.user_chat_history.append("\n" + "User: " + user_input + "\n")
                    self.user_chat_history.append("\n" + "AI: " + ai_response + "\n")

                    self.chat_history.extend([HumanMessage(content=user_input), AIMessage(content=ai_response)])

        except Exception as e:
            raise RuntimeError(f"Failed to run chatbot: {str(e)}")
