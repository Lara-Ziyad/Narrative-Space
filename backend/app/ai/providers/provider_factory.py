from typing import Tuple
from .openai_provider import OpenAIProvider
from .anthropic_provider import  AnthropicProvider
from .ollama_provider import generate_ollama

try:
    from . import NotConfiguredError, ProviderError
except Exception:
    class ProviderError(Exception):
        """Generic provider error."""
        pass

    class NotConfiguredError(ProviderError):
        """Provider is recognized but not configured (e.g., missing API key)."""
        pass


# Allow only known providers at PR4 scope
ALLOWED_PROVIDERS = {"openai", "anthropic", "google", "ollama"}

def parse_model_spec(raw: str) -> Tuple[str, str]:
    """
    [NS-STEP6-PR4] Strict parsing for 'provider:modelId' with legacy support.

    Accept:
      - 'provider:modelId'
      - legacy 'provider.modelId'  -> normalize to 'provider:modelId'
      - legacy 'modelId' only      -> assume provider='openai'

    Reject:
      - empty/undefined values
      - unknown providers (not in ALLOWED_PROVIDERS)

    Returns:
      (provider, model_id)
    """

    raw = (raw or "").strip()
    if not raw or "undefined" in raw.lower():
        raise ValueError("Model must be provided as 'provider:modelId'.")

    # Normalize legacy "provider.model" → "provider:model"
    if "." in raw and ":" not in raw:
        left, right = raw.split(".", 1)
        raw = f"{left}:{right}"

    provider, sep, model_id = raw.partition(":")
    if not sep:
        # legacy form: only model provided → default provider 'openai'
        provider, model_id = "openai", provider

    provider = (provider or "").strip().lower()
    model_id = (model_id or "").strip()

    if not provider or not model_id:
        raise ValueError("Invalid model string; expected 'provider:modelId'.")

    if provider not in ALLOWED_PROVIDERS:
        allowed = ", ".join(sorted(ALLOWED_PROVIDERS))
        raise ValueError(f"Unsupported provider '{provider}'. Allowed: {allowed}")

    return provider, model_id

def generate_with_provider(
    raw_model: str,
    *,
    system: str,
    user: str,
    temperature: float = 0.7,
    max_tokens: int = 300,
) -> str:
    """
    Route to the correct provider implementation.

    - OpenAI is enabled now.
    - Other providers (anthropic/google/ollama) will be added in PR5/PR7.
    """
    provider, model_id = parse_model_spec(raw_model)

    if provider == "openai":

       prov = OpenAIProvider()
       return prov.generate(
            model=model_id,
            system=system, user=user, temperature=temperature, max_tokens=max_tokens
            )

    if provider == "anthropic":
        prov = AnthropicProvider()
        return prov.generate(
            model=model_id,
            system=system,
            user=user,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    if provider == "ollama":
        # [NS-STEP6-PR7] dispatch to local/remote Ollama
        return generate_ollama(
            model_id,
            system=system, user=user, temperature=temperature, max_tokens=max_tokens,
        )

    # For known-but-not-yet-configured providers
    raise NotConfiguredError(f"Provider '{provider}' is not configured yet in PR2.")
