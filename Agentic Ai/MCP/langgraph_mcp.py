import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from langchain_core.tools import StructuredTool
from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.graph.message import add_messages
from typing import Annotated,TypedDict
from langchain_core.messages import AnyMessage
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
class AgentState(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]

load_dotenv()
llm=ChatGroq(
    api_key=os.getenv("API_KEY"),
    model="openai/gpt-oss-120b",
    temperature=0
)


async def main():
    async with streamable_http_client("http://127.0.0.1:8000/mcp") as (read_stream,write_stream):
        async with ClientSession(read_stream,write_stream)as session:
            await session.initialize()
            tools=await session.list_tools()
            async def call_mcp_tool(filename:str):
                result = await session.call_tool(
                    "get_file_content",
                    {"filename":filename}
                )
                return result.structured_content["result"]
            langchain_tool=StructuredTool.from_function(
                coroutine=call_mcp_tool,
                name="get_file_content",
                description="Return the content of a project file"

            )
            tool_node=ToolNode([langchain_tool])
            llm_with_tools=llm.bind_tools([langchain_tool])
            def llm_node(state:AgentState):
                response=llm_with_tools.invoke(state["messages"])
                return {"messages":[response]}
            graph=StateGraph(AgentState)
            graph.add_node("llm",llm_node)
            graph.add_node("tools",tool_node)

            graph.add_edge(START,"llm")

            graph.add_conditional_edges("llm",tools_condition)

            graph.add_edge("tools","llm")

            app=graph.compile()

            result = await app.ainvoke(
                {
                    "messages":[
                        {
                            "role":"user",
                            "content":"Read auth.py and tell me what is inside it."
                        }
                    ]
                }
            )
            print(result["messages"][-1].content)


if __name__=="__main__":
    asyncio.run(main())