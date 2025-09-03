
import os
from datetime import datetime, timezone
from typing import Dict, List, Any


def is_available(provider: str) -> bool:
    """
    Return whether a provider is currently configured (env-based).
    Adjust logic as your deployment needs evolve.
    """
    if provider == "openai":
        return bool(os.getenv("OPENAI_API_KEY"))
    if provider == "anthropic":
        return bool(os.getenv("ANTHROPIC_API_KEY"))
    if provider == "google":
        return bool(os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))
    if provider == "ollama":
        # Treat Ollama as available when host is provided.
        # If you prefer optimistic default, change to: return True
        return bool(os.getenv("OLLAMA_HOST"))
    return False


def required_env(provider: str) -> List[str]:
    """
    Return a list of env vars users need to set to enable the provider.
    This drives clearer UI messages like “missing ANTHROPIC_API_KEY”.
    """
    if provider == "openai":
        return ["OPENAI_API_KEY"]
    if provider == "anthropic":
        return ["ANTHROPIC_API_KEY"]
    if provider == "google":
        return ["GOOGLE_API_KEY (or GEMINI_API_KEY)"]
    if provider == "ollama":
        return ["OLLAMA_HOST (optional if default)"]
    return []


def describe(provider: str, model_id: str) -> str:
    """
    Short, human-readable description per model.
    You can refine these over time without touching the route handlers.
    """
    if provider == "openai":
        if model_id == "gpt-4o":
            return "OpenAI GPT-4o: multimodal, strong quality; text output."
        if model_id == "gpt-4o-mini":
            return "OpenAI GPT-4o-mini: fast & cost-efficient; text output."
        if model_id == "gpt-4.1-mini":
            return "OpenAI GPT-4.1-mini: lightweight reasoning; text output."
        return "OpenAI text model."
    if provider == "anthropic":
        return "Anthropic Claude (Haiku): fast & concise; text output."
    if provider == "google":
        return "Google Gemini 1.5 Pro: long context; text output."
    if provider == "ollama":
        return "Local LLaMA via Ollama; requires local model pull."
    return "Text model."


def capabilities(provider: str, model_id: str) -> Dict[str, bool]:
    """
    Binary capability flags; keep it simple and useful for UI toggles.
    """
    is_vision = (provider == "openai" and model_id in {"gpt-4o", "gpt-4o-mini"})
    return {
        "text_generation": True,
        "vision_input": is_vision,
        "rag_ready": True,  # We inject context before sending, so RAG works uniformly.
    }


def curated_models() -> List[Dict[str, Any]]:
    """
    The curated set used across the app. Enriched with description, capabilities, and availability.
    """
    base = [
        {"provider": "openai",    "id": "gpt-4.1-mini"},
        {"provider": "openai",    "id": "gpt-4o-mini"},
        {"provider": "openai",    "id": "gpt-4o"},
        {"provider": "anthropic", "id": "claude-3-haiku"},
        {"provider": "google",    "id": "gemini-1.5-pro"},
        {"provider": "ollama",    "id": "llama3"},
    ]

    enriched: List[Dict[str, Any]] = []
    for m in base:
        p, mid = m["provider"], m["id"]
        enriched.append({
            "provider": p,
            "id": mid,
            "label": m.get("label") or mid,  # UI shows id-only
            "description": describe(p, mid),
            "capabilities": capabilities(p, mid),
            "available": is_available(p),
            "requires": required_env(p),
            # Leave limits as None for now to avoid incorrect claims
            "limits": {
                "context_window": None,
                "max_output_tokens": None,
            },
            # Mark a sensible default for text (tweak to taste)
            "default_for": ["text"] if (p == "openai" and mid == "gpt-4o-mini") else [],
        })
    return enriched


def now_iso() -> str:
    """UTC timestamp for meta blocks."""
    return datetime.now(timezone.utc).isoformat()
