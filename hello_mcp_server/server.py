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


from .azure_provider import AzureResourceProvider
from .header_middleware import HeaderMiddleware

ISSUER = os.environ["ISSUER"]
AUDIENCE = os.environ.get("AUDIENCE")
SCOPE = os.environ.get("SCOPE").split(" ")

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
    # ①  injects request.user / request.auth by calling provider.load_access_token
    Middleware(
        AuthenticationMiddleware,
        backend=BearerAuthBackend(provider=provider),
    ),
    # ②  your own header middleware
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
