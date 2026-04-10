"""Root orchestrator agent \u2014 coordinates 5 subagents and PDF generation."""

import asyncio
import json
from typing import Any

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from .subagents import (
    ai_visibility,
    technical_seo,
    content_quality,
    schema_markup,
    platform_readiness,
)

ROOT_AGENT_INSTRUCTION = """
You are a senior GEO/SEO audit orchestrator. Your role:

1. Receive a URL from the user
2. Coordinate the following 5 specialist subagents IN PARALLEL:
   - ai_visibility: Analyzes AI training data presence, citation frequency, entity signals
   - technical_seo: Analyzes Core Web Vitals, mobile, HTTPS, speed, sitemap, robots
   - content_quality: Analyzes readability, E-E-A-T, entity density, content depth
   - schema_markup: Validates JSON-LD, FAQPage, HowTo, Article, Organization schemas
   - platform_readiness: Checks readiness for Google AIO, ChatGPT, Gemini, Perplexity

3. Collect all findings and scores from each subagent
4. Compute an overall GEO score (0-100 weighted average)
5. Generate a PDF report using the generate_pdf tool
6. Return the PDF path and a JSON summary

For each subagent tool, pass the target URL and instruct them to return structured findings:
{
  "agent": "<agent_name>",
  "score": 0-100,
  "findings": [{"category": "...", "issue": "...", "severity": "high|medium|low", "recommendation": "..."}],
  "recommendations": ["..."]
}

Use the run_in_sandbox tool to execute Python code for web scraping, data analysis, and PDF generation.
Use the fetch_url tool to retrieve web pages.
Use the write_file and read_file tools to manage files in the sandbox.
"""


def _build_subagent_tool(name: str, agent_module: Any) -> FunctionTool:
    """Build a FunctionTool that runs a subagent and returns structured JSON.

    Args:
        name: Tool name (e.g., "ai_visibility")
        agent_module: The subagent module with get_agent(tools)

    Returns:
        A FunctionTool that executes the subagent and returns JSON
    """
    # Import here to avoid circular deps
    from google.adk.runners import Runner
    from google.adk.sessions.in_memory_session_service import InMemorySessionService

    async def run_subagent(url: str) -> str:
        """Run a subagent and return its structured JSON result."""
        # Build the subagent with no tools (it will use the root agent's tools)
        subagent = agent_module.get_agent([])

        app = type("SubAgentApp", (), {"name": f"{name}_app", "root_agent": subagent})()
        session_service = InMemorySessionService()
        runner = Runner(app=app, session_service=session_service)

        session = await session_service.create_session(
            app_name=app.name,
            user_id="orchestrator",
        )

        from google.genai import types

        prompt = f"""
Analyze the following URL for {name}. Return ONLY a JSON object with this exact structure:
{{
  "agent": "{name}",
  "score": <0-100 integer>,
  "findings": [
    {{"category": "...", "issue": "...", "severity": "high|medium|low", "recommendation": "..."}}
  ],
  "recommendations": ["..."]
}}

URL to audit: {url}

Use any available tools to analyze the URL. Be thorough and return actual findings.
"""

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

        # Try to extract JSON from response
        try:
            # Look for JSON block
            start = result_text.find("{")
            end = result_text.rfind("}") + 1
            if start != -1 and end > start:
                json_str = result_text[start:end]
                parsed = json.loads(json_str)
                return json.dumps(parsed, indent=2)
        except (json.JSONDecodeError, ValueError):
            pass

        return result_text

    return FunctionTool(func=run_subagent)


def get_root_agent(
    sandbox_tools: Any,
    fetch_url_tool: FunctionTool,
    generate_pdf_tool: FunctionTool,
) -> Agent:
    """Build the root orchestrator agent with all tools wired.

    Args:
        sandbox_tools: SandboxTools instance (run_in_sandbox, write_file, read_file)
        fetch_url_tool: ADK FunctionTool for fetch_url
        generate_pdf_tool: ADK FunctionTool for generate_pdf

    Returns:
        Configured root Agent
    """
    # Build subagent tools
    ai_visibility_tool = _build_subagent_tool("ai_visibility", ai_visibility)
    technical_seo_tool = _build_subagent_tool("technical_seo", technical_seo)
    content_quality_tool = _build_subagent_tool("content_quality", content_quality)
    schema_markup_tool = _build_subagent_tool("schema_markup", schema_markup)
    platform_readiness_tool = _build_subagent_tool("platform_readiness", platform_readiness)

    tools = [
        sandbox_tools.run_in_sandbox,
        sandbox_tools.write_file,
        sandbox_tools.read_file,
        fetch_url_tool,
        generate_pdf_tool,
        ai_visibility_tool,
        technical_seo_tool,
        content_quality_tool,
        schema_markup_tool,
        platform_readiness_tool,
    ]

    return Agent(
        name="geo_audit_orchestrator",
        model="gemini-2.5-flash",
        instruction=ROOT_AGENT_INSTRUCTION.strip(),
        tools=tools,
    )
