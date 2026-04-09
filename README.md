# Geo Audit ADK Agent

Google ADK Agent for GEO/SEO site audits with professional PDF report generation.

## Overview

An AI-powered audit agent that analyzes websites for Generative Engine Optimization (GEO) and traditional SEO. Uses 5 parallel subagents to assess AI visibility, technical foundations, content quality, structured data, and platform readiness.

## Quick Start

```bash
# Install dependencies
pip install -e .

# Run the agent
python -m geo_audit_agent.main

# Or use the CLI
python -m geo_audit_agent.cli audit https://example.com
```

## Features

- **5 Parallel Subagents** — AI Visibility, Technical, Content, Schema, Platform
- **PDF Reports** — Professional client-ready documents with charts and gauges
- **GEO Scoring** — 0-100 score with category breakdown
- **Platform Readiness** — ChatGPT, Perplexity, Gemini, Google AIO specific recommendations

## Project Structure

```
geo_audit_adk/
├── src/geo_audit_agent/
│   ├── main.py           # ADK entry point
│   ├── agent.py          # Root agent orchestrator
│   ├── subagents/        # 5 parallel subagents
│   ├── tools/            # PDF, fetching, analysis tools
│   └── skills/           # Geo-seo-claude ported skills
├── tests/
├── docs/
└── SPEC.md
```

## Documentation

- [SPEC.md](./SPEC.md) — Technical specification
- [docs/SETUP.md](./docs/SETUP.md) — Installation guide
- [docs/DEV.md](./docs/DEV.md) — Development guide

## License

MIT
