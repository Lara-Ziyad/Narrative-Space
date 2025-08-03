from .templates import get_prompt_template  # ← استخدم النقطة (import نسبي)

style = "philosophical"
prompt = "A spiraling staircase that leads to nowhere"
context = "From 'The Poetics of Space' by Gaston Bachelard..."

final_prompt = get_prompt_template(style).format(context=context, prompt=prompt)
print("🔹 Final Prompt:\n")
print(final_prompt)
