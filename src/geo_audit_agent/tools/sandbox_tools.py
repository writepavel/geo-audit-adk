"""OpenSandbox tools — run_in_sandbox, write_file, read_file.

These are ADK tools that execute inside ephemeral OpenSandbox containers.
Uses httpx REST API directly — no opensandbox SDK dependency needed.
"""

import asyncio
import httpx
from datetime import timedelta
from typing import Any

from ..config import Settings


# ---------------------------------------------------------------------------
# Internal httpx client
# ---------------------------------------------------------------------------

class OpenSandboxClient:
    """Lightweight REST client for the OpenSandbox API."""

    BASE_PATH = "/api/v1"

    def __init__(self, domain: str, api_key: str, timeout: int = 120):
        self.base_url = f"https://{domain}"
        self.headers = {"x-api-key": api_key, "Content-Type": "application/json"}
        self.timeout = timeout

    # -------------------------------------------------------------------
    # Sandbox lifecycle
    # -------------------------------------------------------------------

    async def create_sandbox(
        self, image: str, timeout_seconds: int = 3600
    ) -> dict[str, Any]:
        """Create a new ephemeral sandbox and return its info dict."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{self.base_url}{self.BASE_PATH}/sandboxes",
                headers=self.headers,
                json={
                    "image": image,
                    "timeout": f"{timeout_seconds}s",
                },
            )
            resp.raise_for_status()
            return resp.json()

    async def get_sandbox(self, sandbox_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(
                f"{self.base_url}{self.BASE_PATH}/sandboxes/{sandbox_id}",
                headers=self.headers,
            )
            resp.raise_for_status()
            return resp.json()

    async def wait_until_ready(self, sandbox_id: str, poll_interval: float = 1.0, timeout: float = 60.0) -> dict[str, Any]:
        """Poll until the sandbox is Running."""
        deadline = asyncio.get_event_loop().time() + timeout
        while True:
            info = await self.get_sandbox(sandbox_id)
            state = info.get("status", {}).get("state", "")
            if state == "Running":
                return info
            if asyncio.get_event_loop().time() > deadline:
                raise TimeoutError(f"Sandbox {sandbox_id} did not become ready in {timeout}s (state={state})")
            await asyncio.sleep(poll_interval)

    async def kill_sandbox(self, sandbox_id: str) -> None:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.delete(
                f"{self.base_url}{self.BASE_PATH}/sandboxes/{sandbox_id}",
                headers=self.headers,
            )
            resp.raise_for_status()

    # -------------------------------------------------------------------
    # Commands
    # -------------------------------------------------------------------

    async def run_command(self, sandbox_id: str, command: str) -> dict[str, Any]:
        """Run a shell command and return execution result."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{self.base_url}{self.BASE_PATH}/sandboxes/{sandbox_id}/commands/run",
                headers=self.headers,
                json={"command": command},
            )
            resp.raise_for_status()
            return resp.json()

    # -------------------------------------------------------------------
    # Files
    # -------------------------------------------------------------------

    async def write_file(self, sandbox_id: str, path: str, content: str) -> None:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{self.base_url}{self.BASE_PATH}/sandboxes/{sandbox_id}/files/write",
                headers=self.headers,
                json={"path": path, "content": content},
            )
            resp.raise_for_status()

    async def read_file(self, sandbox_id: str, path: str) -> str:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(
                f"{self.base_url}{self.BASE_PATH}/sandboxes/{sandbox_id}/files/read",
                headers=self.headers,
                params={"path": path},
            )
            resp.raise_for_status()
            return resp.text


# ---------------------------------------------------------------------------
# ADK tool wrappers
# ---------------------------------------------------------------------------

class SandboxTools:
    """Holds sandbox instance + ADK-compatible async tool callables."""

    def __init__(self, client: OpenSandboxClient, sandbox_id: str):
        self.client = client
        self.sandbox_id = sandbox_id

    async def run_in_sandbox(self, command: str) -> str:
        """Run a shell command in OpenSandbox and return the combined output.

        Args:
            command: Shell command to execute

        Returns:
            Combined stdout and stderr output
        """
        result = await self.client.run_command(self.sandbox_id, command)

        # Parse the result dict — fields may be logs[], stdout, stderr, exit_code
        logs = result.get("logs", [])
        stdout_lines = [m.get("text", "") for m in logs if m.get("stream") == "stdout"]
        stderr_lines = [m.get("text", "") for m in logs if m.get("stream") == "stderr"]

        error = result.get("error")

        output = "\n".join(stdout_lines).strip()
        if stderr_lines:
            output = "\n".join([output, "[stderr]\n" + "\n".join(stderr_lines)]).strip()
        if error:
            output = "\n".join([output, f"[error] {error}"]).strip()
        return output or "(no output)"

    async def write_file(self, path: str, content: str) -> str:
        """Write a file inside the sandbox.

        Args:
            path: Absolute path where to write the file
            content: File content as string

        Returns:
            Confirmation message
        """
        await self.client.write_file(self.sandbox_id, path, content)
        return f"wrote {len(content)} bytes to {path}"

    async def read_file(self, path: str) -> str:
        """Read a file from the sandbox.

        Args:
            path: Absolute path to the file

        Returns:
            File content as string
        """
        return await self.client.read_file(self.sandbox_id, path)


# ---------------------------------------------------------------------------
# Public factory (called by the agent root)
# ---------------------------------------------------------------------------

async def create_sandbox_and_tools(settings: Settings) -> tuple[str, SandboxTools]:
    """Create an OpenSandbox instance and return ADK-compatible tools.

    Returns:
        Tuple of (sandbox_id, SandboxTools) — caller uses sandbox_id to
        pass to destroy_sandbox() when done.
    """
    client = OpenSandboxClient(
        domain=settings.sandbox_domain,
        api_key=settings.sandbox_api_key,
    )

    info = await client.create_sandbox(
        image=settings.sandbox_image,
        timeout_seconds=3600,
    )
    sandbox_id: str = info["id"]

    # Wait for the pod to be Running before accepting commands
    await client.wait_until_ready(sandbox_id, poll_interval=1.0, timeout=60.0)

    tools = SandboxTools(client, sandbox_id)
    return sandbox_id, tools


async def destroy_sandbox(sandbox_id: str, settings: Settings) -> None:
    """Destroy a sandbox by ID."""
    client = OpenSandboxClient(
        domain=settings.sandbox_domain,
        api_key=settings.sandbox_api_key,
    )
    try:
        await client.kill_sandbox(sandbox_id)
    except Exception:
        pass  # Best-effort
