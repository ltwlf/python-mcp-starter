"""
Hello World MCP package.

This package provides a simple MCP (Model Context Protocol) server that can be run
in either stdio or SSE (Server-Sent Events) mode.
"""

from hello_mcp_server.server import mcp, main, run_stdio, run_sse

__version__ = "0.1.0"
__all__ = ["mcp", "main", "run_stdio", "run_sse"]
