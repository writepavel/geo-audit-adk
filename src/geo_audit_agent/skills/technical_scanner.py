"""Technical SEO Scanner skill — runs technical checks.

Ported from geo-seo-claude technical-seo-scanner skill.
"""

TECHNICAL_SCAN_PROMPT = """
## Technical SEO Scanner Skill

Run comprehensive technical SEO checks on a URL.

### Checks

1. **HTTP/HTTPS**: Is it HTTPS? Certificate valid?
2. **Core Web Vitals proxies**:
   - Response time (TTFB) via headers
   - Resource sizes (img, css, js)
   - Render-blocking scripts
3. **Mobile**:
   - Viewport meta tag
   - Touch-friendly tap targets
   - Font size legibility
4. **URL Structure**:
   - SEO-friendly (no long query strings)
   - Consistent hyphens
   - Logical depth (< 3 clicks from home)
5. **Meta Tags**:
   - Title tag (50-60 chars)
   - Meta description (150-160 chars)
   - OG/Twitter cards
6. **Semantic HTML**:
   - Header hierarchy (single H1)
   - Schema.org JSON-LD
   - ARIA landmarks

### Output
{
    "technical_score": 0-100,
    "passed_checks": ["..."],
    "failed_checks": ["..."],
    "warnings": ["..."],
    "critical_issues": ["..."],
}
"""
