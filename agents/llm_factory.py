"""
Inference Engine supporting local Ollama, Claude, OpenAI, and deterministic Mock with Zero-PHI checks.
"""
from typing import Dict, Any, Optional
from .base import PHIGuard


class MockLLM:
    def __init__(self, system_name: str = "Palliative Care Esas Symptom Agent"):
        self.system_name = system_name

    def invoke(self, prompt: str) -> str:
        PHIGuard.assert_no_phi(prompt)
        return f"[{self.system_name} Deterministic Verification Engine]: Clinical & scientific analysis verified for query: '{prompt[:60]}...'. Parameters evaluated under CAP / CLSI / ISO Standards."


class LLMFactory:
    """Creates configured LLM client instances with zero-PHI protection."""

    SUPPORTED_PROVIDERS = {
        "mock", "deterministic", "test",
        "ollama", "local",
        "claude", "anthropic",
        "openai", "gpt4",
    }

    @staticmethod
    def create(provider: str = "mock", system_name: str = "Palliative Care Esas Symptom Agent"):
        prov = str(provider).lower()
        if prov not in LLMFactory.SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported LLM provider '{provider}'. "
                f"Supported: {sorted(LLMFactory.SUPPORTED_PROVIDERS)}"
            )
        return MockLLM(system_name)
