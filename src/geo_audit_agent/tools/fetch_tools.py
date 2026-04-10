"""Web fetching tool — HTTP GET with headers and basic parsing.

Uses httpx inside the OpenSandbox to fetch URLs.
"""

import json
from typing import Any


async def fetch_url(url: str) -> dict[str, Any]:
    """Fetch a URL and return structured data.

    This tool is meant to be used inside OpenSandbox via run_in_sandbox.
    It runs a Python script that uses httpx to fetch the URL.

    Args:
        url: The URL to fetch

    Returns:
        dict with keys: status_code, headers, body, error
    """
    # This is designed to be called via run_in_sandbox with a Python script
    # The actual implementation runs in the sandbox
    fetch_script = f"""
import httpx
import sys

try:
    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        response = client.get("{url}")
        result = {{
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.text[:10000],  # limit body size
            "url": str(response.url),
        }}
        print(json.dumps(result))
except Exception as e:
    print(json.dumps({{"error": str(e), "url": "{url}"}}))
    sys.exit(1)
"""
    return {"script": fetch_script, "note": "Run via run_in_sandbox"}


def build_fetch_script(url: str) -> str:
    """Build the httpx fetch script for a given URL."""
    return f"""
import httpx
import json

url = {json.dumps(url)}

with httpx.Client(timeout=30.0, follow_redirects=True) as client:
    response = client.get(url)
    result = {{
        "status_code": response.status_code,
        "url": str(response.url),
        "content_type": response.headers.get("content-type", ""),
        "body": response.text[:15000],
    }}
    print(json.dumps(result, indent=2))
"""
