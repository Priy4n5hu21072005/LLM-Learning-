import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from langchain_core.tools import StructuredTool
from pydantic import create_model,Field
async def main():
    async with streamable_http_client(
        "http://127.0.0.1:8000/mcp"
    ) as (read_stream,write_stream):
        async with ClientSession(
            read_stream,write_stream
        )as session:
            await session.initialize()

            tools=await session.list_tools()
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
                        mcp_tool.name,
                        kwargs
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

            for mcp_tool in tools.tools:
                tool=create_langchain_tool(mcp_tool)
                langchain_tools.append(tool)

            for tool in langchain_tools:
                print(tool.name)

            for tool in langchain_tools:
                if tool.name =="search_file":
                    result=await tool.ainvoke(
                        {
                            "filename":"auth.py",
                            "keyword":"login"
                        }
                    )
                    print(result)

            print(result)
if __name__=="__main__":
    asyncio.run(main())