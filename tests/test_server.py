from mcp.shared.memory import (
    create_connected_server_and_client_session as client_session,
)
from fastmcp.server import FastMCP


class TestServer:
    async def test_create_server(self):
        server = FastMCP()
        assert server.name == "FastMCP"


def tool_fn(x: int, y: int) -> int:
    return x + y


class TestServerTools:
    async def test_add_tool(self):
        server = FastMCP()
        server.add_tool(tool_fn)
        server.add_tool(tool_fn)
        assert len(server._tool_manager.list_tools()) == 1

    async def test_list_tools(self):
        server = FastMCP()
        server.add_tool(tool_fn)
        async with client_session(server._mcp_server) as client:
            tools = await client.list_tools()
            assert len(tools.tools) == 1

    async def test_call_tool(self):
        server = FastMCP()
        server.add_tool(tool_fn)
        async with client_session(server._mcp_server) as client:
            result = await client.call_tool("my_tool", {"arg1": "value"})
            assert "error" not in result
            assert len(result.content) > 0