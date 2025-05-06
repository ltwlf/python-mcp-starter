"""
Main entry point for the hello_world MCP application.
This file contains the runner functions and CLI code.
"""
import os
import sys
import anyio
import click
import uvicorn
from hello_mcp_server.server import mcp, app

# Runners
async def run_stdio():
    await mcp.run_stdio_async()

def run_sse(host: str, port: int):
    uvicorn.run(app, host=host, port=port)

# CLI
@click.command()
@click.option("--sse", is_flag=True, help="Start as SSE server (otherwise stdio).")
@click.option("--host", default=lambda: os.getenv("HOST", "0.0.0.0"),
              show_default=True, help="Host for SSE mode")
@click.option("--port", type=int, default=lambda: int(os.getenv("PORT", 8000)),
              show_default=True, help="Port for SSE mode")
def main(sse: bool, host: str, port: int):
    if sse:
        run_sse(host, port)
    else:
        anyio.run(run_stdio)

if __name__ == "__main__":
    sys.exit(main())
