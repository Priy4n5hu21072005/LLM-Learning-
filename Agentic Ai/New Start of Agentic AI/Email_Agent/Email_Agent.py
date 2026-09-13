from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
import os
from dotenv import load_dotenv

load_dotenv()



AI = ChatGroq(
    api_key=os.getenv("API_KEY"),
    model="openai/gpt-oss-120b"
)

@tool
def get_wallet_info(email: str) -> str:
    """Get the Wallet type of a MultiWallet user"""
    return "Primary Wallet"

@tool
def get_user_profile(email:str)->str:
    """"Get the Basic Information of multiwallet user"""
    return """
        Name:Priyanshu
        Account Status:Active
        """


LLM_with_tools = AI.bind_tools([get_wallet_info,get_user_profile])

tools = {
    "get_wallet_info": get_wallet_info,
    "get_user_profile":get_user_profile
}
event="USER REGISTER"
message = [
    {
        "role": "user",
        "content": """
        Create a welcome message for Priyanshu.

        You MUST call get_user_profile first using his email.
        After receiving its result, you MUST call get_wallet_info
        using the same email.
        
        event:{event}

        Only after both tools have returned their results,
        create the final welcome message.

        His email is priyanshukumar08357@gmail.com.
        """
    }
]

# Custom Agent
while True:

    response = LLM_with_tools.invoke(message)

    print("AI RESPONSE:", response)

    message.append(response)

    if not response.tool_calls:
        break

    # Tool Execute
    
    for tool_call in response.tool_calls:

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool = tools[tool_name]
        tool_result = tool.invoke(tool_args)
        print("TOOL RESULT:", tool_result)
        message.append(
            ToolMessage(
                content=tool_result,
                tool_call_id=tool_call["id"]
            )
        )

print("FINAL ANSWER:")
print(response.content)
