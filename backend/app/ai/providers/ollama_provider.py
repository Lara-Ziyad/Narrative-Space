import os
import json
import time
from typing import Optional
import requests
from flask import current_app
from . import ProviderBase, NotConfiguredError, ProviderError

DEFAULT_OLLAMA = "http://localhost:11434"  # Ollama default

def _backoff_sleep(i: int, base: float = 0.6) -> None:
    time.sleep(base * (2 ** i) + 0.05 * i)

class OllamaProvider(ProviderBase):
    """
    Calls Ollama's /api/generate with:
      POST { model, prompt, stream:false, options:{ temperature, num_predict }, system? }
    Expects a single JSON object response (non-stream).
    """

    def __init__(self, host: Optional[str] = None) -> None:
        # [NS-STEP6-PR7] Try to get host from Flask app, then env, then default
        host_from_app = getattr(current_app, "ollama_host", None)
        self._host = (host or host_from_app or os.environ.get("OLLAMA_HOST") or DEFAULT_OLLAMA).rstrip("/")
        # Very light sanity check
        if not self._host.startswith("http"):
            raise NotConfiguredError("OLLAMA_HOST must be an http(s) URL")

    def generate(
        self,
        *,
        model: str,
        system: str,
        user: str,
        temperature: float = 0.7,
        max_tokens: int = 300,
    ) -> str:
        url = f"{self._host}/api/generate"
        payload = {
            "model": model,
            # Combine system + user like we do مع المزودات الأخرى
            "prompt": f"<<SYS>>\n{system}\n<</SYS>>\n{user}",
            "stream": False,
            "options": {
                "temperature": float(temperature),
                "num_predict": int(max_tokens),
            },
        }

        last_exc = None
        for attempt in range(3):  # [NS-STEP6-PR7] simple retries
            try:
                resp = requests.post(url, json=payload, timeout=30)
                if resp.status_code == 404:
                    raise NotConfiguredError(f"Ollama endpoint not found at {url}")
                if resp.status_code >= 400:
                    raise ProviderError(f"Ollama HTTP {resp.status_code}: {resp.text}")

                data = resp.json()
                # Ollama returns {"response":"...","done":true,...}
                txt = data.get("response", "")
                if not isinstance(txt, str):
                    txt = json.dumps(data, ensure_ascii=False)
                return txt
            except requests.exceptions.ConnectionError as e:
                last_exc = e
                # service unreachable
                if attempt >= 2:
                    raise NotConfiguredError(f"Ollama host unreachable: {self._host}") from e
                _backoff_sleep(attempt)
            except Exception as e:
                last_exc = e
                if attempt >= 2:
                    raise ProviderError(str(e)) from e
                _backoff_sleep(attempt)
        # Shouldn't reach here
        raise ProviderError(str(last_exc) if last_exc else "Unknown Ollama error")


# [NS-STEP6-PR7] Thin wrapper (keeps parity if your factory calls functions)
def generate_ollama(
    model: str,
    *,
    system: str,
    user: str,
    temperature: float = 0.7,
    max_tokens: int = 300,
) -> str:
    prov = OllamaProvider()
    return prov.generate(
        model=model,
        system=system,
        user=user,
        temperature=temperature,
        max_tokens=max_tokens,
    )
