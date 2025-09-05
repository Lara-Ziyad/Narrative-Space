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
        app.logger.warning(f"[NS-STEP6] Anthropic client init failed: {e}")
