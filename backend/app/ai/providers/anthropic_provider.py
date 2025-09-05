from flask import current_app
from . import ProviderBase, NotConfiguredError, ProviderError

class AnthropicProvider(ProviderBase):
    def __init__(self, client=None) -> None:
        # Reuse shared client from Flask app factory
        self._client = client or getattr(current_app, "anthropic_client", None)
        if self._client is None:
            raise NotConfiguredError("Anthropic client is not configured.")

    def generate(
        self,
        *,
        model: str,
        system: str,
        user: str,
        temperature: float = 0.7,
        max_tokens: int = 300,
    ) -> str:
        try:
            # Anthropic Messages API (Claude 3.x)
            resp = self._client.messages.create(
                model=model,
                system=system,
                messages=[{"role": "user", "content": user}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            # Extract first text block (common shape)
            parts = getattr(resp, "content", []) or []
            for p in parts:
                if getattr(p, "type", "") == "text" and getattr(p, "text", ""):
                    return p.text
            # Fallback: stringify response
            return str(resp)
        except RuntimeError as e:
            # Missing app.anthropic_client or context issues
            raise NotConfiguredError(str(e)) from e
        except Exception as e:
            raise ProviderError(str(e)) from e
