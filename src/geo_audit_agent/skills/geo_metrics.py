"""GEO Metrics Collector skill — analyzes AI visibility signals.

Ported from geo-seo-claude geo-metrics-collector skill.
"""

GEO_METRICS_PROMPT = """
## GEO Metrics Collector Skill

You collect AI visibility metrics for a given URL.

### Data Sources (simulated analysis):
1. **Content signals**: Analyze HTML for AI-preferred content patterns:
   - FAQ sections (AI loves FAQ content)
   - HowTo sections
   - Structured lists and definitions
   - Short, direct answers to questions

2. **Entity signals**: Check for named entities (people, organizations, locations)
   - Organization schema
   - Person schema
   - Article schema with author

3. **Authority signals**:
   - Author credentials and bio pages
   - Citation-ready content (with sources/references)
   - Original research / data

4. **Accessibility signals**:
   - RSS/Atom feed presence
   - Sitemap.xml
   - robots.txt not blocking AI crawlers

### Output Format

Return a dict:
{
    "ai_visibility_score": 0-100,
    "citation_potential": "high|medium|low",
    "entity_score": 0-100,
    "authority_score": 0-100,
    "accessibility_score": 0-100,
    "top_strengths": ["..."],
    "top_weaknesses": ["..."],
}
"""


def analyze_geo_metrics(url: str, html_content: str) -> dict:
    """Analyze GEO metrics for given HTML content."""
    # This function is designed to run inside OpenSandbox
    # Returns a dict with AI visibility metrics
    pass  # Implementation in sandbox
