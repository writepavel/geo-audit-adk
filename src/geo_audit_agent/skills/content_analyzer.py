"""Content Analyzer skill — analyzes content quality and SEO optimization.

Ported from geo-seo-claude content-analyzer skill.
"""

CONTENT_ANALYZER_PROMPT = """
## Content Analyzer Skill

Analyze content quality for GEO/SEO.

### Metrics

1. **Keyword Optimization**:
   - Primary keyword in title, H1, first 100 words
   - Keyword density (1-3% ideal)
   - LSI keywords present

2. **Readability**:
   - Flesch-Kincaid Grade Level (target: 6-8)
   - Average sentence length (< 25 words)
   - Paragraph length (< 150 words)
   - Active voice percentage

3. **E-E-A-T Signals**:
   - Author name present
   - Author bio/page link
   - Publication date
   - Review/citation links
   - Trust signals (about page, contact)

4. **Content Structure**:
   - H1-H6 hierarchy correct
   - Lists and tables used appropriately
   - Images with alt text
   - Internal links

5. **Entity Analysis**:
   - Named entity density
   - Topic diversity
   - Co-occurring entities

### Output
{
    "content_score": 0-100,
    "keyword_score": 0-100,
    "readability_score": 0-100,
    "eeat_score": 0-100,
    "structure_score": 0-100,
    "improvements": ["..."],
}
"""
