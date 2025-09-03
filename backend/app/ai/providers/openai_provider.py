# [NS-STEP6-PR2] OpenAI provider isolated behind a single function.
from flask import current_app

def generate_openai(model_id: str, *, system: str, user: str, temperature: float = 0.7, max_tokens: int = 300) -> str:
    """
    Call OpenAI chat completions using the app-wide client.
    Raises Exception if the client is missing or the API fails.
    """
    client = getattr(current_app, "openai_client", None)
    if client is None:
        raise RuntimeError("OpenAI client is not configured on app.")

    resp = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content
