# [NS-STEP6] Provider clients bootstrap (OpenAI / Anthropic)
import os
from flask import Flask

def attach_openai(app: Flask) -> None:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        setattr(app, "openai_client", None)  # type: ignore[attr-defined]
        return
    try:
        from openai import OpenAI
        setattr(app, "openai_client", OpenAI(api_key=key))  # type: ignore[attr-defined]
    except Exception as e:
        setattr(app, "openai_client", None)  # type: ignore[attr-defined]
        app.logger.warning(f"[NS-STEP6] OpenAI client init failed: {e}")

def attach_anthropic(app: Flask) -> None:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        setattr(app, "anthropic_client", None)  # type: ignore[attr-defined]
        return
    try:
        from anthropic import Anthropic
        setattr(app, "anthropic_client", Anthropic(api_key=key))  # type: ignore[attr-defined]
    except Exception as e:
        setattr(app, "anthropic_client", None)  # type: ignore[attr-defined]
        app.logger.warning(f"Anthropic client init failed: {e}")

def attach_ollama(app: Flask) -> None:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        setattr(app, "anthropic_client", None)  # type: ignore[attr-defined]
        return
    try:
        from anthropic import Anthropic
        setattr(app, "ollama_client", Anthropic(api_key=key))  # type: ignore[attr-defined]
    except Exception as e:
        setattr(app, "ollama_client", None)  # type: ignore[attr-defined]
        app.logger.warning(f"Ollama client init failed: {e}")

def attach_gemini(app: Flask) -> None:
    key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        setattr(app, "gemini_on", False)  # type: ignore[attr-defined]
        return
    try:
        import google.generativeai as genai  # type: ignore
        genai.configure(api_key=key)  # SDK is global; we just mark it on
        setattr(app, "gemini_on", True)  # type: ignore[attr-defined]
    except Exception as e:
        setattr(app, "gemini_on", False)  # type: ignore[attr-defined]
        app.logger.warning(f"[NS-STEP6] Gemini init failed: {e}")