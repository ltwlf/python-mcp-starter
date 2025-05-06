from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.middleware import Middleware
import os

from .header_middleware import HeaderMiddleware

mcp = FastMCP("hello")

@mcp.tool()
def say_hello(name: str) -> str:
    return f"Hello, {name}!"

messages_path = "/messages/"

public_host = os.getenv("PUBLIC_HOST")
sse_url = f"{public_host}{messages_path}" if public_host else "http://localhost:8000/messages/"
sse = SseServerTransport(sse_url)

async def handle_sse(scope, receive, send):
    async with sse.connect_sse(scope, receive, send) as streams:
        await mcp._mcp_server.run(
            *streams, mcp._mcp_server.create_initialization_options()
        )

app = Starlette(
    routes=[
        Mount("/sse", app=handle_sse),
        Mount(messages_path, app=sse.handle_post_message),
    ],
    middleware=[Middleware(HeaderMiddleware)],
)