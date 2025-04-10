import subprocess
from mcp.server.fastmcp import FastMCP

USER_AGENT = "EXECUTE_PYTHON"
mcp_server = FastMCP(USER_AGENT)

@mcp_server.tool(name="execute_python_code", description="执行python代码")
async def execute_python_code(code: str) -> str:
    try:
        process = subprocess.run(['python', '-c', code], capture_output=True, text=True, timeout=10)
        if process.returncode == 0:
            return process.stdout.strip()
        else:
            return f"Error: {process.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "Error: Python code execution timed out."
    except FileNotFoundError:
        return "Error: Python interpreter not found."
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp_server.run(transport="stdio")
