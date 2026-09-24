import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    async with streamable_http_client(
        "http://127.0.0.1:8000/mcp"
    ) as (read_stream,write_stream):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            resource=await session.list_resources()
            print("Available resources: ")

            for resource in resource.resources:
                print(resource.uri)

            resource_data=await session.read_resource("project://file")
            print("\n Resource Content:")
            print(resource_data)

            prompts = await session.list_prompts()

            print("\nAvailable prompts:")
            for prompt in prompts.prompts:
                print(prompt.name)

            result = await session.call_tool(
                "get_file_content",
                {"filename":"auth.py"}
            )
            print(result)

asyncio.run(main())
