from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.middleware import Middleware
import os
from mcp.server.auth.settings import AuthSettings
from mcp.server.auth.middleware.bearer_auth import (
    RequireAuthMiddleware, BearerAuthBackend
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware

load_dotenv()

from .azure_provider import AzureResourceProvider
from .header_middleware import HeaderMiddleware

ISSUER = os.environ.get("ISSUER")
AUDIENCE = os.environ.get("AUDIENCE")
SCOPE = os.environ.get("SCOPE").split(" ")

print(f"ISSUER: {ISSUER}")

provider = AzureResourceProvider(ISSUER, AUDIENCE)

mcp = FastMCP(
    "hello",
    auth_server_provider=provider,
    auth=AuthSettings(
        issuer_url=ISSUER,
        required_scopes=SCOPE,
        authorization_endpoint_enabled=False,
        token_endpoint_enabled=False,
        client_registration_options=None,
        revocation_options=None,
    ),
)


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

middleware = [
    # Add CORS middleware to handle cross-origin requests
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure this to be more restrictive in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(
        AuthenticationMiddleware,
        backend=BearerAuthBackend(provider=provider),
    ),
    Middleware(HeaderMiddleware),
]


routes = [
    Mount("/sse", RequireAuthMiddleware(handle_sse, SCOPE), name="sse"),
    Mount("/messages/",
          RequireAuthMiddleware(sse.handle_post_message, SCOPE)),
]

app = Starlette(
    routes=routes,
    middleware=middleware,
)
