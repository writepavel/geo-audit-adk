# GEO Audit ADK Agent

Google ADK Agent for GEO/SEO site audits with professional PDF report generation.

## Overview

An AI-powered audit agent that analyzes websites for Generative Engine Optimization (GEO) and traditional SEO. Uses 5 parallel subagents to assess AI visibility, technical foundations, content quality, structured data, and platform readiness. Produces a client-ready PDF report with a 0-100 GEO score.

## Quick Start

```bash
pip install -e .
cp .env.example .env
# Edit .env with your API keys

python -m geo_audit_agent.main audit https://example.com
```

## Features

- **5 Parallel Subagents** — AI Visibility, Technical, Content, Schema, Platform Readiness
- **PDF Reports** — Professional documents with charts and gauges
- **GEO Scoring** — 0-100 overall score with category breakdown
- **OpenSandbox Execution** — Secure code execution via ephemeral containers

## Architecture

```
Root Agent (geo_audit_orchestrator)
├── AI Visibility Agent
├── Technical SEO Agent
├── Content Quality Agent
├── Schema Markup Agent
└── Platform Readiness Agent
```

## Documentation

- [SPEC.md](./SPEC.md) — Full technical specification
- [docs/SETUP.md](./docs/SETUP.md) — Installation guide
- [docs/DEV.md](./docs/DEV.md) — Development guide
- [docs/OPENSTANDBOX.md](./docs/OPENSTANDBOX.md) — OpenSandbox details

## License

MIT
