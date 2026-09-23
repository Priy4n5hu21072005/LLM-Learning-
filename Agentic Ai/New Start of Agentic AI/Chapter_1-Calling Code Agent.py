
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.messages import HumanMessage,ToolMessage


API_KEY="YOUR_GROQ_API_KEY"
LLM=ChatGroq(
    api_key=API_KEY,
    model="openai/gpt-oss-120b"
)

@tool
def given_the_country_phone_number(country:str)->str:
    '''Give the phone Startting number of the country like india - +91'''
    response=LLM.invoke(f"the country of {country} phone number code is:")
    '''Return Only calling code nothing else'''
    return response.content


tools=[given_the_country_phone_number]
LLM_WITH_TOOLS=LLM.bind_tools(
    tools,
)

message=[
    HumanMessage(
        content = input("Please Enter the country Name")
    )
]


while True:
    #LLM ko decide karne dena hai ki what to do 
    response=LLM_WITH_TOOLS.invoke(message)

    #LLM Ka response ko memory mein add karna
    message.append(response)

    # ye dekhna ki llm ko tool chayie ki nahi 
    if not response.tool_calls:
        break
    for tool_call in response.tool_calls:
        if tool_call["name"]=="given_the_country_phone_number":
            result=given_the_country_phone_number.invoke(
                tool_call["args"]
            )

        message.append(
            ToolMessage(
                content=result,
                tool_call_id=tool_call["id"]
            )
        )

final_response=LLM.invoke(message)
print(final_response.content)
