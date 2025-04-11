import os
import json
import asyncio

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

from MCP_StdioClient import MCPClient
from common.logger import logger

# 加载 .env 文件，确保 API Key 受到保护
load_dotenv(find_dotenv())

base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")
llm_model_name = os.getenv("MODEL")


async def run_agent(llm, mcp_client, query):
    messages = []
    messages.append({"role": "user", "content": query})
    try:
        response = llm.chat.completions.create(
                        model=llm_model_name,
                        messages=messages,
                        tools=mcp_client.all_tools,
                        tool_choice="auto"
                    )
        response_content = response.choices[0]
        response_message = response_content.message
        if response_content.finish_reason == "tool_calls":
            tool_calls = response_message.tool_calls
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_arguments = json.loads(tool_call.function.arguments)
                
                tool_result = await mcp_client.call_mcp_tool(tool_name, tool_arguments)
                messages.extend([
                    {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [tool_call]
                    },
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result.content[0].text
                    }
                ])
            final_response = llm.chat.completions.create(
                model=llm_model_name,
                messages=messages
            )
            logger.info(f"\n🤖 model: {final_response.choices[0].message.content}")
        else:
            logger.info(f"\n🤖 model: {response_message.content}")
    except Exception as e:
        logger.error(f"Agent 运行错误: {e}")


async def main(servers_list):
    llm = OpenAI(api_key=api_key, base_url=base_url)

    mcp_client = MCPClient()

    await mcp_client.connect_to_servers(servers_list)

    # client循环对话
    while True:
        user_input = input("User: ")
        
        if user_input in ['quit', '退出']:
            break
        
        await run_agent(llm, mcp_client, user_input)
    
    await mcp_client.cleanup()


if __name__ == "__main__":
    
    os.chdir(os.path.dirname(__file__))
    
    servers_list = {
        "exec_py": "./mcp_servers/python/exec_py.py",
        "search_bing": "./mcp_servers/python/search_bing.py",
        "exec_js": "./mcp_servers/js/exec_js.js"
    }
    asyncio.run(main(servers_list))
