from abc import ABC, abstractmethod

from typing import Optional


class ProviderError(Exception):
    """Generic provider error."""
    pass


class NotConfiguredError(ProviderError):
    """Provider is recognized but not configured (e.g., missing API key)."""
    pass


class ProviderBase(ABC):
    """Common interface for text generation providers."""

    @abstractmethod
    def generate(
        self,
        *,
        model: str,
        system: str,
        user: str,
        temperature: float = 0.7,
        max_tokens: int = 300,
    ) -> str:
        """Return the generated text."""
        raise NotImplementedError