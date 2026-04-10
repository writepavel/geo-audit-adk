"""Tests for sandbox_tools.py."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from geo_audit_agent.tools.sandbox_tools import build_sandbox_tools


class TestSandboxTools:
    """Tests for OpenSandbox tools."""

    def test_build_sandbox_tools_returns_list(self):
        """build_sandbox_tools should return a list of callables."""
        mock_sandbox = MagicMock()
        tools = build_sandbox_tools(mock_sandbox)
        assert isinstance(tools, list)
        assert len(tools) == 3

    def test_build_sandbox_tools_contains_expected_names(self):
        """Tools should be named correctly."""
        mock_sandbox = MagicMock()
        tools = build_sandbox_tools(mock_sandbox)
        names = [t.__name__ for t in tools]
        assert "run_in_sandbox" in names
        assert "write_file" in names
        assert "read_file" in names

    @pytest.mark.asyncio
    async def test_run_in_sandbox_returns_output(self):
        """run_in_sandbox should return combined stdout/stderr."""
        mock_sandbox = MagicMock()
        mock_execution = MagicMock()
        mock_execution.logs.stdout = [MagicMock(text="hello")]
        mock_execution.logs.stderr = [MagicMock(text="")]
        mock_execution.error = None
        mock_sandbox.commands.run = AsyncMock(return_value=mock_execution)

        tools = build_sandbox_tools(mock_sandbox)
        run_tool = next(t for t in tools if t.__name__ == "run_in_sandbox")

        result = await run_tool("echo hello")
        assert "hello" in result

    @pytest.mark.asyncio
    async def test_run_in_sandbox_with_error(self):
        """run_in_sandbox should include error in output."""
        mock_sandbox = MagicMock()
        mock_execution = MagicMock()
        mock_execution.logs.stdout = [MagicMock(text="")]
        mock_execution.logs.stderr = [MagicMock(text="")]
        mock_execution.error = MagicMock()
        mock_execution.error.name = "ExitCode"
        mock_execution.error.value = "1"
        mock_sandbox.commands.run = AsyncMock(return_value=mock_execution)

        tools = build_sandbox_tools(mock_sandbox)
        run_tool = next(t for t in tools if t.__name__ == "run_in_sandbox")

        result = await run_tool("false")
        assert "[error]" in result

    @pytest.mark.asyncio
    async def test_write_file_calls_sandbox_files(self):
        """write_file should call sandbox.files.write_file."""
        mock_sandbox = MagicMock()
        mock_sandbox.files.write_file = AsyncMock()

        tools = build_sandbox_tools(mock_sandbox)
        write_tool = next(t for t in tools if t.__name__ == "write_file")

        result = await write_tool("/tmp/test.txt", "hello world")
        mock_sandbox.files.write_file.assert_called_once_with("/tmp/test.txt", "hello world")
        assert "wrote" in result

    @pytest.mark.asyncio
    async def test_read_file_returns_content(self):
        """read_file should return file content."""
        mock_sandbox = MagicMock()
        mock_sandbox.files.read_file = AsyncMock(return_value="file content here")

        tools = build_sandbox_tools(mock_sandbox)
        read_tool = next(t for t in tools if t.__name__ == "read_file")

        result = await read_file("/tmp/test.txt")
        assert result == "file content here"
