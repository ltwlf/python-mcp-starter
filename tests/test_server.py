"""
Tests for the hello_mcp_server MCP server.
"""
import pytest

# Import the actual tool and resource functions from the server
from hello_mcp_server.server import add, get_greeting


@pytest.mark.asyncio
async def test_add_tool():
    """Test the add tool."""
    # Call the actual add function
    result = add(2, 3)
    assert result == 5


@pytest.mark.asyncio
async def test_get_greeting_resource():
    """Test the get_greeting resource."""
    # Call the actual get_greeting function
    result = get_greeting("Copilot")
    assert result == "Hello, Copilot!"
