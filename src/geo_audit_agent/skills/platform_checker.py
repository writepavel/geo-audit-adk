"""Platform Checker skill — checks AI platform compatibility.

Ported from geo-seo-claude platform-checker skill.
"""

PLATFORM_CHECKER_PROMPT = """
## Platform Readiness Checker

Check compatibility with major AI platforms.

### Platforms

1. **Google AI Overview (SGE/AIO)**:
   - High-quality, factual content
   - FAQ schema
   - Clear headings (H2/H3)
   - Cited sources/links
   - Mobile-first, fast loading

2. **Bing Copilot / ChatGPT Plugins**:
   - robots.txt not blocking GPTBot
   - OpenAPI manifest (/well-known/ai-plugin.json)
   - Structured data
   - FAQ content

3. **Perplexity AI**:
   - FAQ and Q&A format
   - Definitive answers (not vague)
   - Citable facts and data
   - Short paragraphs with clear claims

4. **Google Gemini**:
   - Schema.org markup
   - Structured data
   - Content in indexable format

5. **Claude (Anthropic)**:
   - robots.txt not blocking Claude bot
   - Clear, well-structured content
   - Authoritative sources

### Checks

- robots.txt analysis (AI bot access)
- Feed availability (RSS/Atom)
- Sitemap presence
- Content update frequency signals
- API/structured data accessibility

### Output
{
    "platform_readiness_score": 0-100,
    "google_aio_score": 0-100,
    "chatgpt_score": 0-100,
    "perplexity_score": 0-100,
    "gemini_score": 0-100,
    "claude_score": 0-100,
    "blockers": ["..."],
    "recommendations": ["..."],
}
"""
