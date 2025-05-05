import os
import anyio
import click
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP

APP_ID = "hello-mcp-server"
mcp = FastMCP(APP_ID)

# Minimal Starlette app for SSE
starlette_app = Starlette(routes=[Mount("/", app=mcp.sse_app())])

# Example tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

