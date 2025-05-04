# Use Python 3.10 or later
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Expose the port used by the MCP server in SSE mode
EXPOSE 8000

# Command to run the MCP server in SSE mode
CMD ["python", "-m", "hello_mcp_server", "--sse", "--host", "0.0.0.0", "--port", "8000"]

# To run in stdio mode instead (for example, when used as a sidecar),
# use: CMD ["python", "-m", "hello_mcp_server"]
