# mcp_client_module.py
import asyncio
import os
import json
from typing import Optional, Dict, List, Any
from contextlib import AsyncExitStack
import logging
from fastmcp import Client

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MCPClient:
    def __init__(self):
        """初始化 MCP 客户端"""
        self.exit_stack = AsyncExitStack()
        self.sessions: Dict[str, Client] = {}
        self.tool_by_session: Dict[str, list] = {}
        self.all_tools: List[Dict[str, Any]] = []

    async def connect_to_servers(self, servers: dict):
        """同时启动多个server并获取工具"""
        for server_name, server_file in servers.items():
            try:
                session = await self.connect_to_server(server_file)
                logger.info(f"⭕ - {server_name}: {servers[server_name]}")
                self.sessions[server_name] = session
                
                async with session:
                    session_tools = await session.list_tools()
                    self.tool_by_session[server_name] = session_tools
                    for tool in session_tools:
                        function_name = f"{server_name}-{tool.name}"
                        self.all_tools.append({
                            "type": "function",
                            "function": {
                                "name": function_name,
                                "description": tool.description,
                                "parameters": tool.inputSchema,
                                "required": list(tool.inputSchema.keys()) if tool.inputSchema else []
                            }
                        })
            except Exception as e:
                logger.error(f"❌ - 连接到 {server_name} 失败: {str(e)}")
                continue

        logger.info("\n所有可用工具信息：")
        for tool in self.all_tools:
            logger.info(f" - {tool['function']['name']}: {tool['function']['description']}")

    async def connect_to_server(self, server_script_path: str):
        """连接到 MCP 服务器"""
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("服务器脚本必须是 .py 或 .js 文件")

        try:
            client = Client(server_script_path)
            return client
        except Exception as e:
            logger.error(f"⚠️ 连接服务器 {server_script_path} 失败: {e}")
            raise

    async def call_mcp_tool(self, tool_full_name: str, tool_args: dict) -> Optional[Any]:
        """根据工具名称和参数调用 MCP 工具，并处理错误"""
        parts = tool_full_name.split("-")
        if len(parts) != 2:
            logger.warning(f"⚠️ 工具名称格式错误: {tool_full_name}，应为 'server_name-tool_name'")
            return None
        server_name, tool_name = parts
        session = self.sessions.get(server_name)
        if session is None:
            logger.warning(f"⚠️ 未连接到服务器 {server_name} 来执行工具 {tool_full_name}")
            return None
        if server_name not in self.tool_by_session or tool_name not in [_.name for _ in self.tool_by_session[server_name]]:
            logger.warning(f"⚠️ 服务器 {server_name} 不支持工具 {tool_name}")
            return None
        logger.info(f"正在调用工具 {tool_full_name}，参数: {tool_args}")
        try:
            resp = await session.call_tool(tool_name, tool_args)
            return resp
        except Exception as e:
            logger.error(f"⚠️ 调用工具 {tool_full_name} 失败: {e}")
            return None

    async def cleanup(self):
        """清理资源"""
        await self.exit_stack.aclose()
