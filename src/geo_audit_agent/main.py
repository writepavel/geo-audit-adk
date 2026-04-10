"""CLI entry point for the GEO Audit ADK Agent."""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Load .env file if present
env_path = Path(".env")
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

from .agent import root_agent
from .config import get_settings
from .tools.sandbox_tools import build_sandbox_tools


async def run_audit(url: str) -> dict:
    """Run a full GEO audit for the given URL.

    Returns a dict with audit_id, scores, findings, pdf_path.
    """
    settings = get_settings()
    settings.validate()

    from .tools.sandbox_tools import create_sandbox_and_tools

    sandbox, sandbox_tools = await create_sandbox_and_tools(settings)

    try:
        async with sandbox:
            # Build agent with sandbox tools
            from google.adk.agents import Agent

            agent = Agent(
                name="geo_audit_orchestrator",
                model=settings.google_adk_model,
                instruction=(
                    "You are a senior GEO/SEO audit orchestrator. "
                    "Coordinate 5 specialist subagents in parallel, collect their findings, "
                    "and produce a comprehensive audit report with a 0-100 GEO score. "
                    "Use the provided tools to analyze the site and generate a PDF report."
                ),
                tools=sandbox_tools,
            )

            app = type("AuditApp", (), {"name": "geo_audit_app", "root_agent": agent})()
            session_service = InMemorySessionService()
            runner = Runner(app=app, session_service=session_service)

            session = await session_service.create_session(
                app_name=app.name,
                user_id="cli_user",
            )

            prompt = (
                f"Run a complete GEO/SEO audit for {url}. "
                f"Use all 5 subagents (AI Visibility, Technical SEO, Content Quality, "
                f"Schema Markup, Platform Readiness) to analyze the site. "
                f"Collect all findings, compute scores, and generate a PDF report at "
                f"{settings.audit_output_dir}/audit_{{timestamp}}.pdf. "
                f"Return the PDF path and a JSON summary of scores."
            )

            content = types.Content(
                role="user",
                parts=[types.Part(text=prompt)],
            )

            responses = []
            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=content,
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            responses.append(part.text)

            result_text = "\n".join(responses)

            # Try to extract PDF path from response
            pdf_path = None
            for line in result_text.split("\n"):
                if "/workspace/audit_" in line or ".pdf" in line.lower():
                    pdf_path = line.strip()
                    break

            return {
                "audit_id": session.id,
                "url": url,
                "response": result_text,
                "pdf_path": pdf_path,
                "timestamp": datetime.utcnow().isoformat(),
            }
    finally:
        await sandbox.kill()
        await sandbox.close()


def main() -> int:
    """CLI main entry point."""
    parser = argparse.ArgumentParser(
        description="GEO Audit ADK Agent — AI-powered GEO/SEO site auditing"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Run a GEO audit for a URL")
    audit_parser.add_argument("url", help="The URL to audit")
    audit_parser.add_argument(
        "--output", "-o", help="Output file for JSON result", default=None
    )

    args = parser.parse_args()

    if args.command == "audit":
        try:
            result = asyncio.run(run_audit(args.url))
            print(json.dumps(result, indent=2))
            if args.output:
                Path(args.output).write_text(json.dumps(result, indent=2))
                print(f"\nResult saved to {args.output}")
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
