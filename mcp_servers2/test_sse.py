import asyncio
from fastmcp import FastMCP
import subprocess


server = FastMCP("test")

@server.tool(name="execute_command_line", description="执行终端命令")
def execute_command_line(cmd):
    result = subprocess.run(cmd)
    if result.stdout:
        return result.stdout
    if result.stderr:
        return result.stderr


if __name__ == "__main__":
    asyncio.run(server.run_sse_async(
        host="0.0.0.0",
        port=8088
    ))
