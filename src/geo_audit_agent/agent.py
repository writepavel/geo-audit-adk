"""Root orchestrator agent — coordinates 5 subagents and PDF generation."""

from google.adk.agents import Agent

# Import subagents to register their tools
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
   - ai_visibility_agent: Analyzes AI training data presence, citation frequency, entity signals
   - technical_seo_agent: Analyzes Core Web Vitals, mobile, HTTPS, speed, sitemap, robots
   - content_quality_agent: Analyzes readability, E-E-A-T, entity density, content depth
   - schema_markup_agent: Validates JSON-LD, FAQPage, HowTo, Article, Organization schemas
   - platform_readiness_agent: Checks readiness for Google AIO, ChatGPT, Gemini, Perplexity

3. Collect all findings and scores from each subagent
4. Compute an overall GEO score (0-100 weighted average)
5. Generate a PDF report using the generate_pdf tool
6. Return the PDF path and a JSON summary

For each subagent, pass the target URL and instruct them to return structured findings:
{
  score: 0-100,
  findings: [{"category": "...", "issue": "...", "severity": "high|medium|low", "recommendation": "..."}],
  recommendations: ["..."]
}

Use the run_in_sandbox tool to execute Python code for web scraping, data analysis, and PDF generation.
Use the fetch_url tool to retrieve web pages.
Use the write_file and read_file tools to manage files in the sandbox.
"""

# Root agent instance — will be initialized with tools at runtime
root_agent: Agent | None = None


def get_root_agent(tools: list) -> Agent:
    """Build the root orchestrator agent with the provided tools."""
    return Agent(
        name="geo_audit_orchestrator",
        model="gemini-2.5-flash",
        instruction=ROOT_AGENT_INSTRUCTION.strip(),
        tools=tools,
    )
