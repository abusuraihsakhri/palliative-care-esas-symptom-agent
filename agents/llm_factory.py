"""
Deterministic placeholder response factory (no external inference providers configured).
"""
from typing import Dict, Any, Optional
from .base import PHIGuard


class MockLLM:
    def __init__(self, system_name: str = "Palliative Care Esas Symptom Agent"):
        self.system_name = system_name

    def invoke(self, prompt: str) -> str:
        PHIGuard.assert_no_phi(prompt)
        return f"[{self.system_name} offline mock]: No clinical analysis was performed. Received query: '{prompt[:60]}...'."


class LLMFactory:
    """Creates only the implemented offline mock with identifier-pattern screening."""

    SUPPORTED_PROVIDERS = {
        "mock", "deterministic", "test",
    }

    @staticmethod
    def create(provider: str = "mock", system_name: str = "Palliative Care Esas Symptom Agent"):
        prov = str(provider).lower()
        if prov not in LLMFactory.SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported LLM provider '{provider}'. "
                "Only the offline mock provider is implemented; remote providers are not configured."
            )
        return MockLLM(system_name)
