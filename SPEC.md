# GEO Audit ADK Agent — Technical Specification

## 1. Project Overview

**Name:** geo-audit-adk  
**Type:** Google ADK Multi-Agent System with PDF Report Generation  
**Core Functionality:** An AI-powered audit agent that analyzes websites for Generative Engine Optimization (GEO) and traditional SEO, using 5 parallel subagents and producing professional PDF reports.  
**Target Users:** SEO specialists, digital marketers, website owners, GEO consultants

---

## 2. Architecture

### 2.1 Agent Hierarchy

```
Root Agent (geo_audit_orchestrator)
├── Subagent: ai_visibility_agent      (parallel)
├── Subagent: technical_seo_agent       (parallel)
├── Subagent: content_quality_agent    (parallel)
├── Subagent: schema_markup_agent      (parallel)
└── Subagent: platform_readiness_agent (parallel)

Tools (available to all agents):
  - run_in_sandbox(command)   — execute in OpenSandbox
  - write_file(path, content)  — write file in sandbox
  - read_file(path)           — read file from sandbox
  - fetch_url(url)            — HTTP GET with headers
  - generate_pdf(audit_data)  — produce PDF via OpenSandbox
```

### 2.2 Technology Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | Google ADK (Agent Development Kit) |
| LLM | Gemini 2.5 Flash (default) |
| Code Execution | OpenSandbox (ephemeral containers) |
| PDF Generation | ReportLab in OpenSandbox |
| Web Fetching | httpx / requests in OpenSandbox |
| Skills Source | geo-seo-claude (ported) |
| Environment | Python 3.11+ |

### 2.3 OpenSandbox Integration

```python
from opensandbox import Sandbox
from opensandbox.config import ConnectionConfig

config = ConnectionConfig(
    domain="sandboxes.resultcrafter.com",
    api_key=os.getenv("SANDBOX_API_KEY"),
    request_timeout=timedelta(seconds=120),
)

sandbox = await Sandbox.create(
    "code-interpreter:v1.0.2",
    connection_config=config,
)
```

---

## 3. Agent Specifications

### 3.1 Root Orchestrator Agent

**Name:** `geo_audit_orchestrator`  
**Model:** `gemini-2.5-flash`  
**Role:** Receives audit request, spawns 5 subagents in parallel, collects results, triggers PDF generation, returns report.

### 3.2 AI Visibility Subagent

**Name:** `ai_visibility_agent`  
**Checks:** AI training data presence, citation frequency in AI answers, entity recognition, author authority signals, source attribution patterns.
**Output:** `{score: 0-100, findings: [], recommendations: []}`

### 3.3 Technical SEO Subagent

**Name:** `technical_seo_agent`  
**Checks:** Core Web Vitals (LCP, FID, CLS), mobile responsiveness, HTTPS, page speed, URL structure, canonical tags, internal linking, XML sitemap, robots.txt.
**Output:** `{score: 0-100, findings: [], recommendations: []}`

### 3.4 Content Quality Subagent

**Name:** `content_quality_agent`  
**Checks:** TF-IDF keyword distribution, readability (Flesch-Kincaid), E-E-A-T signals, entity density, content depth, header hierarchy, NLP entity extraction.
**Output:** `{score: 0-100, findings: [], recommendations: []}`

### 3.5 Schema Markup Subagent

**Name:** `schema_markup_agent`  
**Checks:** JSON-LD schema.org markup, GEO-specific schemas (FAQPage, HowTo, Article, Organization, Person, BreadcrumbList), schema validation, schema coverage.
**Output:** `{score: 0-100, findings: [], recommendations: []}`

### 3.6 Platform Readiness Subagent

**Name:** `platform_readiness_agent`  
**Checks:** Google AI Overview eligibility, Bing Copilot / ChatGPT plugin readiness, Perplexity / Gemini / Claude compatibility, RSS/Atom feed, API accessibility.
**Output:** `{score: 0-100, findings: [], recommendations: []}`

---

## 4. Tools Specification

### 4.1 OpenSandbox Tools (ADK Tools)

```python
async def run_in_sandbox(command: str) -> str:
    execution = await sandbox.commands.run(command)
    return "\n".join(msg.text for msg in execution.logs.stdout)

async def write_file(path: str, content: str) -> str:
    await sandbox.files.write_file(path, content)
    return f"wrote {len(content)} bytes to {path}"

async def read_file(path: str) -> str:
    return await sandbox.files.read_file(path)
```

### 4.2 Web Fetching Tool

Fetch URL and return headers + body using httpx inside the sandbox.

### 4.3 PDF Generation Tool

Generate PDF report using ReportLab inside OpenSandbox. Includes score gauges, radar chart, severity color-coding.

---

## 5. PDF Report Sections

1. Cover Page — Site name, audit date, overall GEO score gauge
2. Executive Summary — Overview, top issues, top wins
3. Overall Score — 0-100 gauge + category breakdown
4. AI Visibility — Score + findings + recommendations
5. Technical SEO — Score + findings + recommendations
6. Content Quality — Score + findings + recommendations
7. Schema Markup — Score + findings + recommendations
8. Platform Readiness — Per-platform readiness
9. Action Plan — Prioritized fixes with effort/impact matrix

---

## 6. Skills (Ported from geo-seo-claude)

| Skill | Description |
|-------|-------------|
| `geo-metrics-collector` | Collects AI visibility metrics |
| `technical-seo-scanner` | Runs technical SEO checks |
| `content-analyzer` | Analyzes content quality |
| `schema-validator` | Validates structured data |
| `platform-checker` | Checks AI platform compatibility |

---

## 7. Data Flow

```
User Input: URL
       │
       ▼
Root Agent receives URL
       │
       ├──────────────────────────────────────────┐
       ▼                                          ▼
Spawn 5 subagents in parallel              Generate audit_id
       │
       ▼
Each subagent: analyze → return scored findings
       │
       ▼
Root agent collects results → synthesizes JSON
       │
       ▼
Trigger generate_pdf tool → ReportLab in OpenSandbox
       │
       ▼
PDF saved to /workspace/audit_{timestamp}.pdf
       │
       ▼
Return PDF path + summary to user
```

---

## 8. Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | Yes | — | Gemini API key |
| `SANDBOX_API_KEY` | Yes | — | OpenSandbox API key |
| `SANDBOX_DOMAIN` | No | `sandboxes.resultcrafter.com` | OpenSandbox server |
| `GOOGLE_ADK_MODEL` | No | `gemini-2.5-flash` | Model name |
| `AUDIT_OUTPUT_DIR` | No | `/workspace` | PDF output directory |

---

## 9. Acceptance Criteria

- [ ] Root agent correctly spawns all 5 subagents in parallel
- [ ] Each subagent returns a structured score (0-100) with findings and recommendations
- [ ] PDF report generates with all 9 sections
- [ ] PDF includes score gauges, radar chart, severity color-coding
- [ ] OpenSandbox tools (run_in_sandbox, write_file, read_file) work correctly
- [ ] CLI accepts URL argument and returns PDF path
- [ ] Project installs cleanly with `pip install -e .`
- [ ] Unit tests cover core agent and tool functionality
