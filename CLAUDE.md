# For Claude (claude-code) AI Coding Agent

This project uses Google ADK for multi-agent GEO/SEO auditing.

## Key Commands

```bash
pip install -e .        # Install in dev mode
pytest tests/ -v        # Run tests
ruff check src/         # Lint
mypy src/               # Type check
```

## Architecture

- `src/geo_audit_agent/agent.py` — Root orchestrator
- `src/geo_audit_agent/subagents/` — 5 parallel subagents
- `src/geo_audit_agent/tools/` — OpenSandbox + PDF tools
- `src/geo_audit_agent/skills/` — Ported geo-seo-claude skills

## Environment

Copy `.env.example` to `.env` and fill in API keys.

## OpenSandbox

Uses `code-interpreter:v1.0.2` image. API at `sandboxes.resultcrafter.com`.
See `docs/OPENSTANDBOX.md` for details.
