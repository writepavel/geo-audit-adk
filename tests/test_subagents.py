"""Tests for subagent modules."""

import pytest
from unittest.mock import MagicMock

from geo_audit_agent.subagents import (
    ai_visibility,
    technical_seo,
    content_quality,
    schema_markup,
    platform_readiness,
)


class TestSubagents:
    """Tests for all 5 subagents."""

    def test_ai_visibility_agent_name(self):
        """AI visibility agent should have correct name."""
        agent = ai_visibility.get_agent([])
        assert agent.name == "ai_visibility_agent"
        assert "AI Visibility" in agent.instruction

    def test_technical_seo_agent_name(self):
        """Technical SEO agent should have correct name."""
        agent = technical_seo.get_agent([])
        assert agent.name == "technical_seo_agent"
        assert "Technical SEO" in agent.instruction

    def test_content_quality_agent_name(self):
        """Content Quality agent should have correct name."""
        agent = content_quality.get_agent([])
        assert agent.name == "content_quality_agent"
        assert "Content Quality" in agent.instruction

    def test_schema_markup_agent_name(self):
        """Schema Markup agent should have correct name."""
        agent = schema_markup.get_agent([])
        assert agent.name == "schema_markup_agent"
        assert "Schema Markup" in agent.instruction

    def test_platform_readiness_agent_name(self):
        """Platform Readiness agent should have correct name."""
        agent = platform_readiness.get_agent([])
        assert agent.name == "platform_readiness_agent"
        assert "Platform Readiness" in agent.instruction

    def test_all_subagents_use_gemini_flash(self):
        """All subagents should use gemini-2.5-flash model."""
        for module in [ai_visibility, technical_seo, content_quality,
                       schema_markup, platform_readiness]:
            agent = module.get_agent([])
            assert agent.model == "gemini-2.5-flash"

    def test_all_subagents_return_findings_structure(self):
        """All subagent instructions mention returning structured findings."""
        for module in [ai_visibility, technical_seo, content_quality,
                       schema_markup, platform_readiness]:
            instruction = module.SUBAGENT_INSTRUCTION
            assert '"score":' in instruction or "score:" in instruction
            assert "findings" in instruction.lower()
            assert "recommendations" in instruction.lower()
