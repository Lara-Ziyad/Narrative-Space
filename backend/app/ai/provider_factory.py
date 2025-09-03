from typing import Tuple
from .providers.openai_provider import generate_openai

class ProviderError(Exception):
    """Generic provider error."""
    pass

class NotConfiguredError(ProviderError):
    """Provider is recognized but not configured (e.g., missing API key)."""
    pass

def parse_model_spec(raw: str) -> Tuple[str, str]:
    """
    Accepts either 'provider:modelId' or 'modelId' (defaults provider to 'openai').
    """
    provider, sep, model_id = raw.partition(":")
    if not sep:  # no provider specified
        return "openai", raw.strip()
    return provider.strip().lower(), model_id.strip()

def generate_with_provider(
    raw_model: str,
    *,
    system: str,
    user: str,
    temperature: float = 0.7,
    max_tokens: int = 300,
) -> str:
    """
    Route the call by provider. For PR2 we support 'openai' only.
    """
    provider, model_id = parse_model_spec(raw_model)

    if provider == "openai":
        try:
            return generate_openai(
                model_id,
                system=system,
                user=user,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except RuntimeError as e:
            # Missing app.openai_client or similar misconfig
            raise NotConfiguredError(str(e)) from e
        except Exception as e:
            raise ProviderError(str(e)) from e

    # Any non-openai provider is not supported in PR2
    raise NotConfiguredError(f"Provider '{provider}' is not configured yet in PR2.")
