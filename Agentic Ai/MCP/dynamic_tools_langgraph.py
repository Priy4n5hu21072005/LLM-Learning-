from typing import TypedDict,Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import START,StateGraph,END
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_groq import ChatGroq
from langchain_core.tools import StructuredTool
import os 
from dotenv import load_dotenv
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from pydantic import create_model,Field

class AgentState(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]

load_dotenv()
llm=ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-120b",
    temperature=0
)
async def main():
    async with streamable_http_client("http://127.0.0.1:8000/mcp")as (read_stream,write_stream):
        async with ClientSession(read_stream,write_stream)as session:
            await session.initialize()
            mcp_tools=await session.list_tools()
            def create_args_model(mcp_tool):
                schema=mcp_tool.input_schema
                field={}
                for name in schema.get("properties",{}):
                    field[name]=(str,Field(...))
                return create_model(
                    f"{mcp_tool.name}Arguments", **field
                )

            def create_langchain_tool(mcp_tool):
                async def call_mcp_tool(**kwargs):
                    result=await session.call_tool(
                        mcp_tool.name,kwargs
                    )
                    if result.structured_content:
                        return result.structured_content.get("result")
                    return result.content[0].text
                args_model=create_args_model(mcp_tool)
                return StructuredTool.from_function(
                    coroutine=call_mcp_tool,
                    name=mcp_tool.name,
                    description=mcp_tool.description,
                    args_schema=args_model
                )

            langchain_tools=[]
            for mcp_tool in mcp_tools.tools:
                tool=create_langchain_tool(mcp_tool)
                langchain_tools.append(tool)


            llm_with_tools=llm.bind_tools(langchain_tools)
            tool_node=ToolNode(langchain_tools)
            

            async def llm_node(state:AgentState):
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
                        (
                            "user","Search for the keyword 'login' inside auth.py."
                        )
                    ]
                }
            )
            print(result["messages"][-1].content)
if __name__=="__main__":
    asyncio.run(main())