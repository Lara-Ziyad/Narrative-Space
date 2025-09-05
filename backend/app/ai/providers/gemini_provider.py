# [NS-STEP6-PR6] Google Gemini provider (class-based, consistent with others)
from flask import current_app
from . import ProviderBase, NotConfiguredError, ProviderError

class GeminiProvider(ProviderBase):
    def __init__(self) -> None:
        # We configure google-generativeai globally during app bootstrap.
        # Here we only check a flag to ensure it happened.
        if not getattr(current_app, "gemini_on", False):
            raise NotConfiguredError("Gemini client is not configured.")
        try:
            import google.generativeai as genai  # type: ignore
            self._genai = genai
        except Exception as e:
            raise NotConfiguredError(f"Gemini SDK import failed: {e}") from e

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
            # Gemini uses a model instance; we pass the system prompt as system_instruction
            mdl = self._genai.GenerativeModel(model, system_instruction=system)
            cfg = {
                "temperature": float(temperature),
                "max_output_tokens": int(max_tokens),
            }
            resp = mdl.generate_content(user, generation_config=cfg)
            # Typical shape: resp.text
            txt = getattr(resp, "text", None)
            if isinstance(txt, str) and txt:
                return txt
            # Fallback: stringify parts
            return str(resp)
        except RuntimeError as e:
            raise NotConfiguredError(str(e)) from e
        except Exception as e:
            raise ProviderError(str(e)) from e
