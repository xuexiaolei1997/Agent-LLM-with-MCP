import { McpServer, ResourceTemplate } from '@modelcontextprotocol/sdk/server/mcp.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { z } from "zod";
z.string()

const server = new McpServer({
    name: "ExecJavascript",
    version: "1.0.0"
});

server.tool("exec_js", 
    "执行js代码",
    { jscode: z.string() }, 
    async ({ jscode }) => {
        try {
            const result = eval(jscode);
            return {content: [{ type: "text", text: String(result)}]};
        } catch ( error ) {
            return { content: [{ type: "error", error: { message: String(error) } }] };
        }
    }
);

server.tool("add",
    "两个数相加",
    { a: z.number(), b: z.number() },
    async ({ a, b }) => ({
      content: [{ type: "text", text: String(a + b) }]
    })
  );

const transport = new StdioServerTransport();
await server.connect(transport);
