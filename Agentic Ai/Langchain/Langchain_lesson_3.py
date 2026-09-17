from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from dotenv import load_dotenv
import os 


load_dotenv()
print(os.getenv("GOOGLE_GEN_AI_API_KEY"))


llm = ChatGoogleGenerativeAI(temperature=0.7,model="gemini-3.5-flash")

chain = llm 

store = {}

def sessionStorage(sessionId:str):
    if sessionId not in store:
        store[sessionId]=InMemoryChatMessageHistory()

    return store[sessionId]

chain_with_memory = RunnableWithMessageHistory(runnable=chain,
                                               sessionStorage=sessionStorage)

while True:

    user_input = input("tell me your name ")

    if user_input.lower()=="exit":
        break

    response = chain_with_memory.invoke(
        [HumanMessage(content = user_input)],
        config={
            "configurable":{"sessionId":"user1"}
        })

    print("AI",response.content)
