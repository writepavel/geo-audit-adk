"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_sandbox():
    """Provide a mock OpenSandbox instance."""
    sandbox = MagicMock()
    sandbox.commands.run = MagicMock()
    sandbox.files.write_file = MagicMock()
    sandbox.files.read_file = MagicMock()
    sandbox.kill = MagicMock()
    sandbox.close = MagicMock()
    return sandbox


@pytest.fixture
def mock_settings():
    """Provide mock settings."""
    from geo_audit_agent.config import Settings
    return Settings(
        google_api_key="test-key",
        sandbox_api_key="test-sandbox-key",
        sandbox_domain="localhost:8080",
    )
