from mcp.server.fastmcp import FastMCP
import requests
from mcp.server.fastmcp import FastMCP

USER_AGENT = "SearchBing-SSE"

settings = {
    "host": "0.0.0.0",
    "port": 8088,
    "log_level": "INFO",
    "debug": False
}

mcp_server = FastMCP(USER_AGENT, **settings)

SERPER_URL = "https://cn.bing.com/"


@mcp_server.tool(name="search_bing", description="通过浏览器查询")
async def search_bing(search_keywords: str):
    response = requests.get(SERPER_URL, params={"q": search_keywords})
    return response.text


if __name__ == "__main__":
    mcp_server.run(transport='sse')
