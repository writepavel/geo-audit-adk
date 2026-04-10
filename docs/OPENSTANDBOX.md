# OpenSandbox Integration

## Overview

This project uses OpenSandbox to provide secure code execution for:
- Web scraping and data fetching
- PDF report generation with ReportLab
- NLP and content analysis
- Running Python scripts for GEO metric computation

## How It Works

1. **Sandbox Creation**: A container is spawned via OpenSandbox REST API
2. **Tool Execution**: ADK agent tools (run_in_sandbox, write_file, read_file) execute inside the sandbox
3. **Lifecycle**: Sandbox lives for the duration of the audit session, then is destroyed

## API Configuration

```python
from opensandbox import Sandbox
from opensandbox.config import ConnectionConfig

config = ConnectionConfig(
    domain="sandboxes.resultcrafter.com",
    api_key=os.getenv("SANDBOX_API_KEY"),
    request_timeout=timedelta(seconds=120),
)

sandbox = await Sandbox.create(
    "code-interpreter:v1.0.2",  # Has Python + Git pre-installed
    connection_config=config,
    timeout=timedelta(minutes=30),
)
```

## Sandbox Image

Default: `sandbox-registry.cn-zhangjiakou.cr.aliyuncs.com/opensandbox/code-interpreter:v1.0.2`

Includes:
- Python 3.x with pip
- Node.js
- Git
- curl, wget
- Various system tools

## Security

- Each audit runs in an isolated ephemeral container
- Containers are destroyed after the audit completes
- No persistent state between audits
- Network access is sandboxed

## Troubleshooting

### Sandbox creation fails
- Check `SANDBOX_API_KEY` is correct
- Verify OpenSandbox server is running at `sandboxes.resultcrafter.com`
- Check network connectivity

### Commands timeout
- Increase `request_timeout` in `ConnectionConfig`
- Break long-running commands into smaller steps

### PDF generation fails
- Ensure ReportLab is installed in the sandbox image
- Check output directory permissions
- Verify `/workspace` directory exists
