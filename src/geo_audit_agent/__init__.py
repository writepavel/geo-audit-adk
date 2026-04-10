"""GEO Audit ADK Agent — multi-agent system for GEO/SEO site auditing."""

__version__ = "0.1.0"
__author__ = "writepavel"

from .agent import root_agent
from .config import Settings, get_settings

__all__ = ["root_agent", "Settings", "get_settings"]
