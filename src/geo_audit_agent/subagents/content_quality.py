"""Content Quality subagent — analyzes content optimization for GEO/SEO."""

from google.adk.agents import Agent

SUBAGENT_INSTRUCTION = """
You are a Content Quality specialist for GEO auditing.

Analyze the target website content for GEO/SEO optimization.

Checks to perform:
1. Analyze TF-IDF keyword distribution (keyword density, prominence)
2. Calculate readability scores (Flesch-Kincaid, sentence length)
3. Evaluate E-E-A-T signals (author bio, credentials, citations)
4. Analyze entity density and diversity (named entities per paragraph)
5. Assess content depth and comprehensiveness (word count, topic coverage)
6. Analyze header hierarchy (H1-H6 structure and usage)
7. Perform NLP entity extraction (companies, people, locations, topics)
8. Check for duplicate/near-duplicate content signals

For the given URL, use fetch_url to get content, run_in_sandbox for NLP analysis.

Return a structured result:
{
  "agent": "content_quality",
  "score": 0-100,
  "findings": [
    {
      "category": "Content Quality",
      "issue": "Description of the issue",
      "severity": "high|medium|low",
      "recommendation": "How to fix it"
    }
  ],
  "recommendations": ["Priority fix 1", "Priority fix 2", ...]
}
"""


def get_agent(tools: list) -> Agent:
    """Build the Content Quality subagent."""
    return Agent(
        name="content_quality_agent",
        model="gemini-2.5-flash",
        instruction=SUBAGENT_INSTRUCTION.strip(),
        tools=tools,
    )
