"""
Debug utilities for hello_mcp_server.

This module provides debugging capabilities for the MCP server.
It should only be used during development and never in production.
"""
import sys
import os
import subprocess
import argparse

# Function kept for compatibility with existing scripts
def inspector_command():
    """
    Run the MCP inspector with debugpy - compatibility function.
    
    This function is maintained for backward compatibility with older scripts.
    It simply calls run_inspector_with_debugpy with default parameters.
    """
    return run_inspector_with_debugpy()

def run_inspector_with_debugpy(wait_for_client=False, port=5678):
    """
    Run the MCP server with inspector and debugpy.
    
    Args:
        wait_for_client: If True, debugpy will wait for a client to attach before running
        port: Debug port to listen on
    """
    # Get the path to the virtual environment's Python interpreter
    venv_python = os.path.abspath(os.path.join(os.getcwd(), ".venv", "bin", "python"))
    
    cmd = [
        "npx", "@modelcontextprotocol/inspector",
        "uv", "run", "-m", "debugpy", "--listen", str(port)
    ]
    
    if wait_for_client:
        cmd.append("--wait-for-client")
        
    cmd.append("./hello_mcp_server/server.py")
    
    # Set environment variables to ensure we're using the virtual environment
    env = os.environ.copy()
    if os.path.exists(venv_python):
        env["PYTHONPATH"] = os.getcwd()
        # If using uv run, we'll use our virtual env
        venv_bin = os.path.dirname(venv_python)
        env["PATH"] = f"{venv_bin}:{env.get('PATH', '')}"
    
    try:
        print(f"Running MCP inspector with command: {' '.join(cmd)}")
        print(f"Debugpy listening on port {port}")
        if wait_for_client:
            print("Waiting for debugger to attach...")
        subprocess.run(cmd, check=True, env=env)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error running inspector: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Inspector process terminated by user")
        return 0

def main():
    """Command-line entry point for the debug module."""
    parser = argparse.ArgumentParser(description="Debug utilities for hello_mcp_server")
    parser.add_argument("--port", type=int, default=5678, 
                        help="Port for debugpy to listen on")
    parser.add_argument("--wait", "--wait-for-client", action="store_true", dest="wait",
                        help="Wait for a debugger to attach before running")
    args = parser.parse_args()
    
    return run_inspector_with_debugpy(wait_for_client=args.wait, port=args.port)

if __name__ == "__main__":
    sys.exit(main())
