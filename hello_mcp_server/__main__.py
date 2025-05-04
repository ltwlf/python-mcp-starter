"""
Main entry point for the hello_world MCP application.
This file simply imports and runs the main function from the server module.
"""
import sys
from hello_mcp_server.server import main

if __name__ == "__main__":
    sys.exit(main())
