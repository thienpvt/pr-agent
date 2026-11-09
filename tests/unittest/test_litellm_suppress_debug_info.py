"""Regression guard for the fork's LiteLLM provider-banner suppression.

`LITELLM.SUPPRESS_PROVIDER_DEBUG_INFO` defaults to True and silences litellm's
raw "Provider List: ..." print() banner; setting it to false must leave
litellm's own default untouched.
"""

from unittest.mock import patch

import litellm
import pytest

import pr_agent.algo.ai_handlers.litellm_ai_handler as litellm_handler


class _FakeBox:
    def __init__(self, values=None):
        self._values = values or {}

    def get(self, key, default=None):
        return self._values.get(key, default)


class _FakeSettings:
    def __init__(self, settings_values=None):
        self.config = _FakeBox({"ai_timeout": 30, "max_model_tokens": 32000, "model": "gpt-4o"})
        self.litellm = _FakeBox()
        self._settings_values = settings_values or {}

    def get(self, key, default=None):
        return self._settings_values.get(key, default)


@pytest.mark.parametrize(("configured", "expected"), [(None, True), (True, True), (False, False)])
def test_suppress_provider_debug_info(monkeypatch, configured, expected):
    settings_values = {}
    if configured is not None:
        settings_values["LITELLM.SUPPRESS_PROVIDER_DEBUG_INFO"] = configured
    monkeypatch.setattr(litellm_handler, "get_settings", lambda: _FakeSettings(settings_values))
    monkeypatch.setattr(litellm, "suppress_debug_info", False)

    with patch("pr_agent.algo.ai_handlers.litellm_ai_handler._require_litellm_interface"):
        litellm_handler.LiteLLMAIHandler()

    assert litellm.suppress_debug_info is expected
