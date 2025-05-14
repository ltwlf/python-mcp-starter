from mcp.server.fastmcp import FastMCP

# Stateless server (no session persistence)
mcp = FastMCP("StatelessServer", stateless_http=True)

@mcp.tool(description="A simple echo tool")
def echo(message: str) -> str:
    return f"Echo: {message}"

def run_server():
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    run_server()