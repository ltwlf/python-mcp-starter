"""
Tests for the hello_mcp_server MCP server.
"""
import pytest

# Import the actual tool and resource functions from the server
from hello_mcp_server.server import say_hello


@pytest.mark.asyncio
async def test_say_hello_tool():
    """Test the add tool."""
    # Call the actual add function
    result = say_hello("Chris")
    assert result == "Hello, Chris!"


