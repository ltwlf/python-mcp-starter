# Python MCP Server Starter Template

A template repository for creating Python applications using the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) and the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk).

## Features

- Implements an MCP server using the `mcp` Python SDK (`FastMCP`).
- Exposes MCP **Tools** (functions callable by LLMs) and **Resources** (data accessible by LLMs).
- Clean, modular architecture
- Easy tool and resource registration
- Command-line interface with customizable options
- Ready for production deployment
- Built-in debug capabilities using debugpy with VS Code integration
- Development tools configured (using `uv` for environment/package management)
- Docker support for containerized deployment

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) (Recommended for environment and package management)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) (Recommended visual tool for testing/debugging MCP servers)
- [Optional] Git
- [Optional] Docker for containerized deployment

### Installation

1.  **Clone or Use as Template:** Get the code.

    ```shell
    git clone https://github.com/ltwlf/python-mcp-starter.git your-repo-name # Or use GitHub's "Use this template" button
    cd your-repo-name
    ```

2.  **Rename the Project:** Rename the core components:
    *   Rename the `hello_mcp_server` directory to your desired Python package name (e.g., `my_awesome_mcp`).
    *   Search and replace `hello-mcp-server` (in `pyproject.toml`, `README.md`, `Dockerfile`, `docker-compose.yml`) with your project name (e.g., `my-awesome-mcp`).
    *   Search and replace `hello_mcp_server` (in Python import statements like in `main.py`, `tests/test_server.py`, `pyproject.toml` scripts section) with your new package name.
    *   Update the `APP_ID` in your renamed `server.py` file.
    *   Update `.vscode/launch.json` configuration file to reflect your new project and package names.

3.  **Create Virtual Environment:**

    ```shell
    # Create the virtual environment
    uv venv
    # Activate the environment (Windows PowerShell)
    .venv\Scripts\Activate.ps1
    # Or for other shells:
    # source .venv/bin/activate  (Linux/macOS)
    # .venv\Scripts\activate.bat (Windows Command Prompt)
    ```

4.  **Install Dependencies:**

    ```shell
    uv pip install -e ".[dev]"
    ```

### Running the MCP Server for Development

You can run the server directly using `uv run` or the `mcp` CLI tool provided by the SDK. This allows testing with tools like the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

#### In stdio mode (for MCP Inspector)

**Method 1: Using `uv run`**
```powershell
# Ensure your virtual environment is active first
# Replace 'hello-mcp-server' with the script name defined in your pyproject.toml
uv run your-script-name
```

**Method 2: Using the `mcp` CLI tool**
```powershell
# Ensure your virtual environment is active first
# Replace 'hello_mcp_server' with your renamed package directory
mcp dev ./your_package_name/server.py
```

#### In SSE mode

```powershell
# Ensure your virtual environment is active first
# Replace 'hello-mcp-server' with your script name
uv run your-script-name --sse
```

Or with custom host and port:

```powershell
# Ensure your virtual environment is active first
# Replace 'hello-mcp-server' with your script name
uv run your-script-name --sse --host 127.0.0.1 --port 9000
```

### Docker Deployment

Update the `Dockerfile` and `docker-compose.yml` to reflect your renamed project/package before building.

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build and run directly with Docker
# Replace 'hello-mcp-server' with your image name
docker build -t your-image-name .
docker run -p 8000:8000 your-image-name
```

## Microsoft Azure Deployment

When deploying to Microsoft Azure App Service, a `requirements.txt` file is needed for the platform to properly install your Python dependencies. While this project uses `uv` for development dependency management, you can generate a compatible `requirements.txt` file using uv:

```bash
# Generate a requirements.txt file from your uv.lock file
uv pip export --requirements > requirements.txt
```

For a successful deployment to Azure App Service:

1. Generate the `requirements.txt` file as shown above
2. Ensure your `startup.sh` file contains the correct command to start your MCP server:
   ```bash
   #!/bin/bash
   python -m hello_mcp_server --sse --host 0.0.0.0 --port 8000
   ```
   Note: Replace `hello_mcp_server` with your actual package name if you renamed it.
3. When deploying to Azure App Service, make sure all these files are included in your deployment package.

## Development

### Debugging

This project includes built-in debugging capabilities using debugpy. There are two main ways to debug your MCP server:

#### Using the Debug Module

The project includes a dedicated debug module that makes debugging easy:

```bash
# Using uv (recommended)
uv run mcp-debug

```
Connect to the MCP Inspector first, and once connected, use the VS Code debug configuration **Attach to MCP worker** to attach the debugger for debugging

#### Using VS Code

VS Code debugging is configured with several launch configurations:

1. **Attach to MCP worker** - Attach to a running MCP server (attach this to a running mcp-debug)
2. **Launch MCP Server (SSE)** - Launch the MCP server directly with server-sent events

For the best experience:
1. First, run `uv run mcp-debug` in a terminal
2. Then, to set breakpoints, use the VS Code debugger with the "Attach to MCP worker" configuration

> **Note:** Make sure you have your virtual environment set up with `uv venv` and `uv pip install -e .[dev]` before debugging.

3. **Check Python interpreter:**
   - Ensure VS Code is using the correct Python interpreter from your virtual environment
   - If needed, select the interpreter using the Python extension's "Select Interpreter" command

To use these configurations:
1. Open the Run and Debug panel in VS Code (Ctrl+Shift+D)
2. Select the desired configuration from the dropdown
3. Click the play button or press F5

#### Security Considerations

- Debug mode should never be used in production environments
- The debugger exposes a network port that could be exploited if not secured
- Always use debugging on trusted networks or with proper security measures in place

### Adding New Tools

Add new tools using the `@mcp.tool()` decorator in `your_package_name/server.py`:

```python
# your_package_name/server.py
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("your-app-id") # Ensure APP_ID matches your project

# ... existing tools ...

# Add your new tool
@mcp.tool()
async def my_new_tool(param1: str, param2: int, ctx: Context) -> dict:
    """
    Description of what your tool does.
    Use the ctx object to report progress, log info, or read resources.
    """
    ctx.info(f"Running my_new_tool with {param1=}, {param2=}")
    # Tool implementation
    result = f"Processed {param1} {param2} times"
    await ctx.report_progress(1, 1) # Example progress
    return {"result": result}
```

### Adding New Resources

Add new resources using the `@mcp.resource()` decorator in `your_package_name/server.py`:

```python
# your_package_name/server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("your-app-id") # Ensure APP_ID matches your project

# ... existing resources ...

# Add resources
@mcp.resource("your-resource-uri")
def your_resource_func():
    """Returns application settings."""
    return {"theme": "dark", "language": "en"}
```

### Testing

Make sure the import statements in `tests/test_server.py` point to your renamed package.

```bash
pytest
```


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [MCP](https://github.com/microsoft/mcp) - Model Context Protocol from Microsoft
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Python implementation for MCP
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) - Tool for inspecting MCP communication