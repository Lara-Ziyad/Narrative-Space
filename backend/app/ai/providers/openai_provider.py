

from flask import current_app
from . import ProviderBase, NotConfiguredError, ProviderError

class OpenAIProvider(ProviderBase):
    def __init__(self, client=None) -> None:
        self._client = client or getattr(current_app, "openai_client", None)
        if self._client is None:
            raise NotConfiguredError("OpenAI client is not configured.")

    def generate(self, *, model: str, system: str, user: str,
                 temperature: float = 0.7, max_tokens: int = 300) -> str:
        try:
            resp = self._client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content or ""
        except RuntimeError as e:
            # Missing app.openai_client or similar misconfig
            raise NotConfiguredError(str(e)) from e

        except Exception as e:
            raise ProviderError(str(e)) from e
