"""Schema Validator skill — validates structured data markup.

Ported from geo-seo-claude schema-validator skill.
"""

SCHEMA_VALIDATOR_PROMPT = """
## Schema Validator Skill

Find and validate JSON-LD schema.org markup.

### GEO-Relevant Schemas

1. **FAQPage** — Highest value for AI citations. Check for:
   - mainEntity.question and mainEntity.acceptedAnswer
   - Both question and answer text present

2. **HowTo** — Step-by-step content. Check for:
   - step: HowToStep or HowToSection
   - text for each step

3. **Article / NewsArticle / BlogPosting**:
n   - headline, author, datePublished, publisher
   - image

4. **Organization**:
   - name, url, logo, sameAs (social links)

5. **Person** (author):
   - name, url, jobTitle, worksFor

6. **BreadcrumbList**:
   - itemListElement with position and name

### Validation Rules
- All required fields present
- Types match schema.org spec
- @id matches canonical URL (for Article)
- @type is singular (not array)
- No syntax errors in JSON-LD

### Output
{
    "schema_score": 0-100,
    "schemas_found": ["FAQPage", "Organization", ...],
    "valid_schemas": ["..."],
    "invalid_schemas": [{"type": "...", "error": "..."}],
    "geo_relevant_missing": ["FAQPage", "HowTo"],
}
"""
