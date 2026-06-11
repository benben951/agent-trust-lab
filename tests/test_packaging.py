from __future__ import annotations

import importlib


def test_copilot_subpackage_is_importable() -> None:
    module = importlib.import_module("agent_trust_lab.copilot")
    assert hasattr(module, "ReviewOrchestrator")
