from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup

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
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    response = requests.get(f"{SERPER_URL}?q={search_keywords}", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    result_elements = soup.select("#b_results > li")
    data = []
    for parent in result_elements:
        if parent.select_one('h2') is None:
            continue
        data.append({
            "title": parent.select_one('h2').text,
            'snippet': parent.select_one('div.b_caption > p').text,
            'link': parent.select_one('div.b_tpcn > a').get('href')
        })
    return [data]


if __name__ == "__main__":
    mcp_server.run(transport='sse')
