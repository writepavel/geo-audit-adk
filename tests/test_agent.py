"""Tests for the root agent and agent.py."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from geo_audit_agent.agent import ROOT_AGENT_INSTRUCTION, get_root_agent


class TestRootAgent:
    """Tests for root orchestrator agent."""

    def test_root_agent_instruction_not_empty(self):
        """Instruction string should not be empty."""
        assert ROOT_AGENT_INSTRUCTION is not None
        assert len(ROOT_AGENT_INSTRUCTION.strip()) > 100

    def test_root_agent_instruction_mentions_subagents(self):
        """Instruction should mention all 5 subagents."""
        instruction = ROOT_AGENT_INSTRUCTION.lower()
        assert "ai visibility" in instruction
        assert "technical seo" in instruction
        assert "content quality" in instruction
        assert "schema markup" in instruction
        assert "platform readiness" in instruction

    def test_get_root_agent_returns_agent(self):
        """get_root_agent should return an Agent instance."""
        mock_tools = [MagicMock(), MagicMock()]
        agent = get_root_agent(mock_tools)
        assert agent is not None
        assert agent.name == "geo_audit_orchestrator"
        assert agent.tools == mock_tools

    def test_get_root_agent_has_correct_model(self):
        """Agent should use gemini-2.5-flash by default."""
        agent = get_root_agent([])
        assert agent.model == "gemini-2.5-flash"
