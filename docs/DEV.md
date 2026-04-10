# Development Guide

## Project Structure

```
src/geo_audit_agent/
├── main.py           # CLI entry point
├── agent.py          # Root orchestrator
├── config.py         # Settings management
├── subagents/        # 5 specialist subagents
│   ├── ai_visibility.py
│   ├── technical_seo.py
│   ├── content_quality.py
│   ├── schema_markup.py
│   └── platform_readiness.py
├── tools/            # ADK tools
│   ├── sandbox_tools.py   # OpenSandbox execution
│   ├── fetch_tools.py    # Web fetching
│   └── pdf_tools.py      # PDF generation
└── skills/           # Ported geo-seo-claude skills
    ├── geo_metrics.py
    ├── technical_scanner.py
    ├── content_analyzer.py
    ├── schema_validator.py
    └── platform_checker.py
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/geo_audit_agent

# Run specific test file
pytest tests/test_agent.py -v
```

## Code Quality

```bash
# Lint with ruff
ruff check src/

# Format with ruff
ruff format src/

# Type check with mypy
mypy src/
```

## Adding a New Subagent

1. Create `src/geo_audit_agent/subagents/my_new_agent.py`
2. Define `SUBAGENT_INSTRUCTION` constant
3. Define `get_agent(tools)` function
4. Import and export in `subagents/__init__.py`
5. Add tests in `tests/test_subagents.py`

## Adding a New Tool

1. Create tool function in appropriate `tools/` module
2. The tool should be an async callable
3. Return string output for ADK compatibility
4. Add tests in `tests/test_tools.py`
