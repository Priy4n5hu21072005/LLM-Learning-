from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
from langchain_core.messages import ToolMessage,HumanMessage
from langchain_core.tools import tool
from schema import EmailResponse

load_dotenv()

llm=ChatGroq(
    api_key=os.getenv("API_KEY"),
    model="openai/gpt-oss-120b"
)
Structured_llm=llm.with_structured_output(EmailResponse)

event=["USER_REGISTERED","WALLET_CREATED","TRANSACTIONS"]
event_data={
    "USER_REGISTERED":{
        "Name":"Priyanshu"
    },
    "WALLET_CREATED":{
        "wallet_type":"saving"
    },
    "TRANSACTIONS":{
        "amount":500,
        "transaction_type":"TRANSFER",
        "wallet_type":"savings"
    }

}

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


LLM_with_tools = llm.bind_tools([get_wallet_info,get_user_profile])

tools = {
    "get_wallet_info": get_wallet_info,
    "get_user_profile":get_user_profile
}

def run_agent(message):
    while True:
        response=LLM_with_tools.invoke(message)
        message.append(response)
        if not response.tool_calls:
            return response.content
        for tool_call in response.tool_calls:
            tool_name=tool_call["name"]
            tool_args=tool_call["args"]
            tool=tools[tool_name]
            tool_result=tool.invoke(tool_args)
            message.append(
                ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_call["id"]
                )
            )


def generate_email_message(name,event,event_data):
    prompt = f"""
        You are the AI Communication Agent for MultiWallet.

        User Name: {name}
        Event: {event}
        Event Data: {event_data}

        Generate an email strictly according to the event:

        USER_REGISTERED:
        - Welcome the user to MultiWallet.
        - Thank them for completing registration.
        - Do not mention transactions or wallets unless provided.

        WALLET_CREATED:
        - Inform the user that their new wallet was created successfully.
        - Mention only wallet details provided in Event Data.
        - Do not invent balances or account details.

        TRANSACTION_COMPLETED:
        - Confirm the transaction.
        - Mention amount, transaction type, wallet and status only if provided.
        - Do not invent transaction details.

        Rules:
        - Use tools only when additional information is genuinely required.
        - Never invent financial data, balances, wallet details, or transaction information.
        - Keep the email professional and concise.
        - Include a Subject line.
        - Return only the final email.
        """
    message=[HumanMessage(content=prompt)]
    final_email=run_agent(message)
    response=Structured_llm.invoke(final_email)
    return response


response = generate_email_message(
    "Priyanshu",
    "TRANSACTION_COMPLETED",
    {
        "amount": 700,
        "transaction_type": "TRANSFER",
        "wallet_type": "Savings",
        "status": "SUCCESS"
    }
)

print(response)
print(response.subject)
print(response.body)

