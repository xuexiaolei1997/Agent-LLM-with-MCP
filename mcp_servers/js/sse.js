import express from "express";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { z } from "zod";

const server = new McpServer({
  name: "example-server",
  version: "1.0.0"
});

// ... set up server resources, tools, and prompts ...

server.tool(
    "test_tool",
    "测试工具",
    { test_data: z.string() },
    async ({ test }) => {
      comsole.log("打印测试数据"+ test_data);
      return {
        content: [{ type: "text", text: test_data }]
      };
    }
  );


const app = express();

// to support multiple simultaneous connections we have a lookup object from
// sessionId to transport
/**
 * @type {Object.<string, SSEServerTransport>} transports
 */
const transports = {};

app.get("/sse", async (_, res) => {
  const transport = new SSEServerTransport('/messages', res);
  transports[transport.sessionId] = transport;
  res.on("close", () => {
    delete transports[transport.sessionId];
  });
  await server.connect(transport);
});

app.post("/messages", async (req, res) => {
  const sessionId = String(req.query.sessionId);
  const transport = transports[sessionId];
  if (transport) {
    await transport.handlePostMessage(req, res);
  } else {
    res.status(400).send('No transport found for sessionId');
  }
});

app.listen(3001);