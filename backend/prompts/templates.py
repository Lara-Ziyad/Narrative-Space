def get_prompt_template(style: str) -> str:
    templates = {
        "poetic": (
            "Compose a poetic narrative describing the following space:\n\n"
            "{context}\n\n"
            "User description: {prompt}"
        ),
        "philosophical": (
            "Reflect philosophically on the nature of the following space:\n\n"
            "{context}\n\n"
            "User description: {prompt}"
        ),
        "critical": (
            "Critique the design and spatial implications of the following:\n\n"
            "{context}\n\n"
            "User description: {prompt}"
        ),
        "fictional": (
            "Write a short fictional story set in the described space:\n\n"
            "{context}\n\n"
            "User description: {prompt}"
        ),
    }

    return templates.get(style, templates["poetic"])
