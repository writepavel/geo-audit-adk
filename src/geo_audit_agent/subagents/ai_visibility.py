"""AI Visibility subagent — analyzes AI training data presence and citation patterns."""

from google.adk.agents import Agent

SUBAGENT_INSTRUCTION = """
You are an AI Visibility specialist for GEO auditing.

Analyze the target website for its presence and visibility in AI systems.

Checks to perform:
1. Simulate AI training data presence (check for sitemap, RSS, structured data)
2. Analyze entity recognition signals (Organization, Person, Article schemas)
3. Assess citation potential (author authority, source attribution patterns)
4. Evaluate content quality signals AI systems use for citations
5. Check for FAQ and HowTo content that AI prefers

For the given URL, use the fetch_url tool to retrieve content, then analyze.

Return a structured result:
{
  "agent": "ai_visibility",
  "score": 0-100,
  "findings": [
    {
      "category": "AI Visibility",
      "issue": "Description of the issue",
      "severity": "high|medium|low",
      "recommendation": "How to fix it"
    }
  ],
  "recommendations": ["Priority fix 1", "Priority fix 2", ...]
}

Use run_in_sandbox to execute analysis code.
"""


def get_agent(tools: list) -> Agent:
    """Build the AI visibility subagent."""
    return Agent(
        name="ai_visibility_agent",
        model="gemini-2.5-flash",
        instruction=SUBAGENT_INSTRUCTION.strip(),
        tools=tools,
    )
