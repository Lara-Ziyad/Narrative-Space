def get_prompt_template(style: str) -> str:
    templates = {
    "poetic": """You are a literary narrator. Write a lyrical, evocative **poem-like** narrative.
- Use imagery, rhythm, and line breaks.
- It's OK to rhyme or alliterate.
Context (may inspire your text):
{context}

User description:
{prompt}
""",
    "philosophical": """You are a reflective thinker. Write a **philosophical essay** about the space.
- Do NOT use verse, rhyme, or line breaks like poetry.
- Use a clear argument, 2–4 short paragraphs, and careful reasoning.
Context (may inform your reasoning):
{context}

User description:
{prompt}
""",
    "critical": """You are a critic. Write a **critical review** of the space.
- Do NOT use poetic devices or line-broken verse.
- Structure: thesis → evidence (from context) → evaluation → conclusion.
Context to consider:
{context}

User description:
{prompt}
""",
    "fictional": """You are a storyteller. Write a brief **scene of fiction** set in the space.
- Narrative prose (no poem form).
- Show, don't tell; 1–3 short paragraphs.
Context (optional inspiration):
{context}

User description:
{prompt}
""",
}

    return templates.get(style, templates["poetic"])
