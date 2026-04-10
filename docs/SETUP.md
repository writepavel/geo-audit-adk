# Setup Guide

## Prerequisites

- Python 3.11+
- Google Gemini API key
- OpenSandbox API key

## Installation

```bash
# Clone the repository
git clone https://github.com/writepavel/geo-audit-adk.git
cd geo-audit-adk

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Copy and configure environment
cp .env.example .env
```

## Environment Variables

Edit `.env` with your API keys:

```bash
GOOGLE_API_KEY=your_gemini_api_key
SANDBOX_API_KEY=your_opensandbox_api_key
SANDBOX_DOMAIN=sandboxes.resultcrafter.com
GOOGLE_ADK_MODEL=gemini-2.5-flash
AUDIT_OUTPUT_DIR=/workspace
```

## Running the Audit

```bash
# Run audit via CLI
python -m geo_audit_agent.main audit https://example.com

# Or install as a package and use
geo-audit audit https://example.com

# Run with custom output
python -m geo_audit_agent.main audit https://example.com --output result.json
```

## Getting API Keys

### Google Gemini API Key
1. Go to Google AI Studio: https://aistudio.google.com/apikey
2. Create a new API key
3. Copy to `GOOGLE_API_KEY`

### OpenSandbox API Key
1. Contact your OpenSandbox administrator
2. Or use the default key for local development: `opensandbox-api-key-change-me`
3. Copy to `SANDBOX_API_KEY`
