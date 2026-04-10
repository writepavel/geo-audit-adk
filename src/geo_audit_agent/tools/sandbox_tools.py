"""OpenSandbox tools — run_in_sandbox, write_file, read_file.

These are ADK tools that execute inside ephemeral OpenSandbox containers.
"""

import os
from datetime import timedelta
from typing import Callable

from opensandbox import Sandbox
from opensandbox.config import ConnectionConfig

from ..config import Settings


async def create_sandbox_and_tools(settings: Settings) -> tuple[Sandbox, list[Callable]]:
    """Create an OpenSandbox instance and return ADK-compatible tools."""
    config = ConnectionConfig(
        domain=settings.sandbox_domain,
        api_key=settings.sandbox_api_key,
        request_timeout=timedelta(seconds=120),
    )

    sandbox = await Sandbox.create(
        settings.sandbox_image,
        connection_config=config,
        timeout=timedelta(minutes=30),
    )

    tools = build_sandbox_tools(sandbox)
    return sandbox, tools


def build_sandbox_tools(sandbox: Sandbox) -> list[Callable]:
    """Build ADK-compatible tools backed by an OpenSandbox instance.

    Returns a list of async callables that can be passed as tools to ADK agents.
    """

    async def run_in_sandbox(command: str) -> str:
        """Run a shell command in OpenSandbox and return the output.

        Args:
            command: Shell command to execute

        Returns:
            Combined stdout and stderr output
        """
        execution = await sandbox.commands.run(command)
        stdout = "\n".join(msg.text for msg in execution.logs.stdout)
        stderr = "\n".join(msg.text for msg in execution.logs.stderr)

        if execution.error:
            stderr = "\n".join(
                [
                    stderr,
                    f"[error] {execution.error.name}: {execution.error.value}",
                ]
            ).strip()

        output = stdout.strip()
        if stderr:
            output = "\n".join([output, f"[stderr]\n{stderr}"]).strip()
        return output or "(no output)"

    async def write_file(path: str, content: str) -> str:
        """Write a file inside the sandbox.

        Args:
            path: Absolute path where to write the file
            content: File content as string

        Returns:
            Confirmation message
        """
        await sandbox.files.write_file(path, content)
        return f"wrote {len(content)} bytes to {path}"

    async def read_file(path: str) -> str:
        """Read a file from the sandbox.

        Args:
            path: Absolute path to the file

        Returns:
            File content as string
        """
        return await sandbox.files.read_file(path)

    return [run_in_sandbox, write_file, read_file]
