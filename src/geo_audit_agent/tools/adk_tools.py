"""ADK tool wrappers for fetch_url and generate_pdf.

These are proper ADK FunctionTool factories that use the SandboxTools
REST client to execute scripts inside OpenSandbox.
"""

import asyncio
import tempfile
from typing import Any

from .fetch_tools import build_fetch_script
from .pdf_tools import build_pdf_script
from .sandbox_tools import SandboxTools


def build_fetch_url_tool(sandbox_tools: SandboxTools) -> Any:
    """Build an ADK FunctionTool for fetch_url.

    Args:
        sandbox_tools: SandboxTools instance with REST client

    Returns:
        An ADK FunctionTool that fetches URLs via the sandbox
    """

    async def fetch_url(url: str) -> str:
        """Fetch a URL using httpx inside OpenSandbox.

        Args:
            url: The URL to fetch

        Returns:
            JSON string with status_code, url, content_type, body
        """
        script = build_fetch_script(url)
        result = await sandbox_tools.run_in_sandbox(f"python3 -c \"{script.replace(chr(34), chr(92) + chr(34))}\"")
        return result

    # Lazy import to avoid circular reference at module load
    from google.adk.tools import FunctionTool

    return FunctionTool(func=fetch_url)


def build_generate_pdf_tool(sandbox_tools: SandboxTools) -> Any:
    """Build an ADK FunctionTool for generate_pdf.

    Args:
        sandbox_tools: SandboxTools instance with REST client

    Returns:
        An ADK FunctionTool that generates PDFs via the sandbox
    """

    async def generate_pdf(audit_data: str, output_path: str) -> str:
        """Generate a PDF audit report using ReportLab.

        Args:
            audit_data: JSON string of audit results
            output_path: Where to save the PDF

        Returns:
            Confirmation message with PDF path
        """
        import json

        try:
            data = json.loads(audit_data)
        except json.JSONDecodeError:
            return f"Error: invalid JSON audit_data: {audit_data[:200]}"

        script = build_pdf_script(data, output_path)

        # Escape the script for shell quoting
        escaped_script = script.replace(chr(34), chr(92) + chr(34)).replace("\n", " ")

        # Write script to temp file and run it (more reliable for multi-line scripts)
        tmp_script_path = "/tmp/gen_pdf.py"
        await sandbox_tools.write_file(tmp_script_path, script)

        result = await sandbox_tools.run_in_sandbox(f"python3 {tmp_script_path}")
        return result

    # Lazy import to avoid circular reference at module load
    from google.adk.tools import FunctionTool

    return FunctionTool(func=generate_pdf)
