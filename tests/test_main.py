"""
Tests for the __main__ module which contains the CLI and runners.
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

import hello_mcp_server.__main__ as main_module


@pytest.fixture
def cli_runner():
    """Fixture for testing click CLI commands."""
    return CliRunner()


@patch('hello_mcp_server.__main__.run_sse')
def test_cli_with_sse_flag(mock_run_sse, cli_runner):
    """Test CLI with the --sse flag."""
    # Run the CLI with the --sse flag
    result = cli_runner.invoke(main_module.main, ['--sse'])
    
    # Check the result
    assert result.exit_code == 0
    
    # Verify that run_sse was called
    mock_run_sse.assert_called_once_with('0.0.0.0', 8000)


@patch('hello_mcp_server.__main__.run_sse')
def test_cli_with_sse_and_custom_host_port(mock_run_sse, cli_runner):
    """Test CLI with the --sse flag and custom host/port."""
    # Run the CLI with the --sse flag and custom host/port
    result = cli_runner.invoke(main_module.main, ['--sse', '--host', '127.0.0.1', '--port', '9000'])
    
    # Check the result
    assert result.exit_code == 0
    
    # Verify that run_sse was called with custom host/port
    mock_run_sse.assert_called_once_with('127.0.0.1', 9000)


@patch('hello_mcp_server.__main__.anyio.run')
def test_cli_without_sse_flag(mock_anyio_run, cli_runner):
    """Test CLI without the --sse flag (stdio mode)."""
    # Run the CLI without the --sse flag
    result = cli_runner.invoke(main_module.main, [])
    
    # Check the result
    assert result.exit_code == 0
    
    # Verify that anyio.run was called with run_stdio
    mock_anyio_run.assert_called_once()
    # The first argument should be the run_stdio function
    assert mock_anyio_run.call_args[0][0] == main_module.run_stdio


@patch('hello_mcp_server.__main__.uvicorn.run')
def test_run_sse(mock_uvicorn_run):
    """Test the run_sse function."""
    main_module.run_sse('127.0.0.1', 8080)
    
    # Verify that uvicorn.run was called with the correct arguments
    mock_uvicorn_run.assert_called_once_with(main_module.starlette_app, host='127.0.0.1', port=8080)


@patch('hello_mcp_server.__main__.mcp.run_stdio_async')
@pytest.mark.asyncio
async def test_run_stdio(mock_run_stdio_async):
    """Test the run_stdio function."""
    await main_module.run_stdio()
    
    # Verify that mcp.run_stdio_async was called
    mock_run_stdio_async.assert_called_once()


@patch.dict(os.environ, {"HOST": "custom.host", "PORT": "9999"})
@patch('hello_mcp_server.__main__.run_sse')
def test_cli_with_environment_variables(mock_run_sse, cli_runner):
    """Test that CLI respects environment variables."""
    # Run the CLI with the --sse flag (should use environment variables for host/port)
    result = cli_runner.invoke(main_module.main, ['--sse'])
    
    # Check the result
    assert result.exit_code == 0
    
    # Verify that run_sse was called with the values from environment variables
    mock_run_sse.assert_called_once_with('custom.host', 9999)
