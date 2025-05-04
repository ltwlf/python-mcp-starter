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

# Runners
async def run_stdio():
    await mcp.run_stdio_async()

def run_sse(host: str, port: int):
    uvicorn.run(starlette_app, host=host, port=port)

# CLI
@click.command()
@click.option("--sse", is_flag=True, help="Start as SSE server (otherwise stdio).")
@click.option("--host", default=lambda: os.getenv("MCP_HOST", "0.0.0.0"),
              show_default=True, help="Host for SSE mode")
@click.option("--port", type=int, default=lambda: int(os.getenv("MCP_PORT", 8000)),
              show_default=True, help="Port for SSE mode")
def main(sse: bool, host: str, port: int):
    if sse:
        run_sse(host, port)
    else:
        anyio.run(run_stdio)

if __name__ == "__main__":
    main()
